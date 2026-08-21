#include <Arduino.h>
#include <FlexCAN_T4.h>
#include <SD.h>
#include <SPI.h>

#if BENI_STAGE0_ENABLE_IMU
#include <Adafruit_BNO08x.h>
#endif

#include "beni_stage0.h"

using beni::stage0::Stage0Record;

namespace {

FlexCAN_T4<CAN1, RX_SIZE_256, TX_SIZE_16> can1;
FlexCAN_T4<CAN2, RX_SIZE_256, TX_SIZE_16> can2;

#if BENI_STAGE0_ENABLE_IMU
Adafruit_BNO08x bno08x(beni::stage0::kBnoResetPin);
sh2_SensorValue_t sensor_value{};
#endif

struct Counters {
  uint32_t can1_tx = 0;
  uint32_t can1_rx = 0;
  uint32_t can2_tx = 0;
  uint32_t can2_rx = 0;
  uint32_t can_errors = 0;
  uint32_t imu_events = 0;
  uint32_t dropped_records = 0;
};

struct ImuLatest {
  int16_t gyro[3] = {};
  int16_t accel[3] = {};
  uint32_t gyro_timestamp = 0;
  uint32_t accel_timestamp = 0;
  bool present = false;
  bool gyro_seen = false;
  bool accel_seen = false;
};

constexpr size_t kRingRecords = 128;
constexpr size_t kWriteRecords = 16;  // 16 * 256 B = one 4 kB SD write.
Stage0Record ring[kRingRecords]{};
size_t ring_head = 0;
size_t ring_tail = 0;
size_t ring_count = 0;

Counters counters;
ImuLatest imu;
File log_file;
bool sd_ready = false;
bool logging = false;
bool sd_write_failed = false;
uint32_t log_started_us = 0;
uint32_t log_bytes = 0;
uint32_t record_sequence = 0;
uint32_t status_flags = 0;
uint32_t can_token = 0;
elapsedMicros sample_clock;
elapsedMicros can_test_clock;
elapsedMillis status_clock;

void print_help() {
  Serial.println("Stage 0 commands:");
  Serial.println("  s  start the 10 minute, 256 kB/s microSD gate");
  Serial.println("  x  stop and close the current microSD test");
  Serial.println("  ?  print status");
  Serial.println("No actuator commands exist in this firmware.");
}

uint32_t elapsed_since(uint32_t then_us) { return micros() - then_us; }

uint32_t flags_now() {
  uint32_t flags = status_flags;
  if (logging) flags |= beni::stage0::kSdActive;
  if (imu.present) flags |= beni::stage0::kImuPresent;
  if (imu.accel_seen) flags |= beni::stage0::kImuRawAccelSeen;
  if (imu.gyro_seen) flags |= beni::stage0::kImuRawGyroSeen;
  return flags;
}

void report_status() {
  Serial.printf(
      "CAN1 tx/rx=%lu/%lu CAN2 tx/rx=%lu/%lu errors=%lu IMU events=%lu "
      "SD=%s bytes=%lu dropped=%lu\n",
      counters.can1_tx, counters.can1_rx, counters.can2_tx, counters.can2_rx,
      counters.can_errors, counters.imu_events, logging ? "ACTIVE" : "idle",
      log_bytes, counters.dropped_records);
}

bool configure_imu_reports() {
#if BENI_STAGE0_ENABLE_IMU
  // The normal accelerometer report is a low-rate keepalive alongside the two
  // raw 1 kHz reports. Only the raw reports are recorded for estimator work.
  const bool accel_keepalive = bno08x.enableReport(SH2_ACCELEROMETER, 10000);
  const bool raw_accel =
      bno08x.enableReport(SH2_RAW_ACCELEROMETER,
                          beni::stage0::kImuReportPeriodUs);
  const bool raw_gyro =
      bno08x.enableReport(SH2_RAW_GYROSCOPE,
                          beni::stage0::kImuReportPeriodUs);
  return accel_keepalive && raw_accel && raw_gyro;
#else
  return false;
#endif
}

void setup_imu() {
#if BENI_STAGE0_ENABLE_IMU
  if (!bno08x.begin_SPI(beni::stage0::kBnoCsPin,
                        beni::stage0::kBnoIntPin)) {
    Serial.println("BNO085 not found; SD and CAN gates remain available.");
    return;
  }
  imu.present = true;
  if (!configure_imu_reports()) {
    Serial.println("BNO085 found, but one or more reports could not be enabled.");
    return;
  }
  Serial.println("BNO085 raw accel/gyro requested at 1 kHz.");
#else
  Serial.println("BNO085 support disabled at compile time.");
#endif
}

void service_imu() {
#if BENI_STAGE0_ENABLE_IMU
  if (!imu.present) return;
  if (bno08x.wasReset() && !configure_imu_reports()) {
    Serial.println("BNO085 reset; report re-enable failed.");
  }
  while (bno08x.getSensorEvent(&sensor_value)) {
    ++counters.imu_events;
    if (sensor_value.sensorId == SH2_RAW_GYROSCOPE) {
      imu.gyro[0] = sensor_value.un.rawGyroscope.x;
      imu.gyro[1] = sensor_value.un.rawGyroscope.y;
      imu.gyro[2] = sensor_value.un.rawGyroscope.z;
      imu.gyro_timestamp = sensor_value.un.rawGyroscope.timestamp;
      imu.gyro_seen = true;
    } else if (sensor_value.sensorId == SH2_RAW_ACCELEROMETER) {
      imu.accel[0] = sensor_value.un.rawAccelerometer.x;
      imu.accel[1] = sensor_value.un.rawAccelerometer.y;
      imu.accel[2] = sensor_value.un.rawAccelerometer.z;
      imu.accel_timestamp = sensor_value.un.rawAccelerometer.timestamp;
      imu.accel_seen = true;
    }
  }
#endif
}

void setup_can() {
  can1.begin();
  can1.setBaudRate(beni::stage0::kCanBaud);
  can2.begin();
  can2.setBaudRate(beni::stage0::kCanBaud);
#if BENI_STAGE0_CAN_INTERNAL_LOOPBACK
  can1.enableLoopBack();
  can2.enableLoopBack();
  Serial.println("CAN1/CAN2 configured for internal loopback at 500 kbit/s.");
#else
#error "Stage 0 must use internal loopback; live-bus transmit is intentionally disabled"
#endif
}

void send_can_test(FlexCAN_T4_Base &bus, uint32_t id, uint32_t token,
                   uint32_t &tx_counter) {
  CAN_message_t message{};
  message.id = id;
  message.len = 8;
  memcpy(message.buf, &token, sizeof(token));
  const uint32_t inverse = ~token;
  memcpy(message.buf + 4, &inverse, sizeof(inverse));
  if (bus.write(message)) {
    ++tx_counter;
  } else {
    ++counters.can_errors;
  }
}
bool valid_can_echo(const CAN_message_t &message, uint32_t expected_id) {
  if (message.id != expected_id || message.len != 8) return false;
  uint32_t token = 0;
  uint32_t inverse = 0;
  memcpy(&token, message.buf, sizeof(token));
  memcpy(&inverse, message.buf + 4, sizeof(inverse));
  return inverse == ~token;
}

void service_can() {
  if (can_test_clock >= 10000) {
    can_test_clock -= 10000;
    ++can_token;
    send_can_test(can1, beni::stage0::kCan1TestId, can_token, counters.can1_tx);
    send_can_test(can2, beni::stage0::kCan2TestId, can_token, counters.can2_tx);
  }

  CAN_message_t message{};
  while (can1.read(message)) {
    if (valid_can_echo(message, beni::stage0::kCan1TestId)) {
      ++counters.can1_rx;
      status_flags |= beni::stage0::kCan1LoopbackOk;
    } else {
      ++counters.can_errors;
    }
  }
  while (can2.read(message)) {
    if (valid_can_echo(message, beni::stage0::kCan2TestId)) {
      ++counters.can2_rx;
      status_flags |= beni::stage0::kCan2LoopbackOk;
    } else {
      ++counters.can_errors;
    }
  }
  can1.events();
  can2.events();
}

bool choose_log_file() {
  char name[16]{};
  for (uint8_t index = 0; index < 100; ++index) {
    snprintf(name, sizeof(name), "STG0_%02u.BIN", index);
    if (!SD.exists(name)) {
      log_file = SD.open(name, FILE_WRITE);
      if (log_file) {
        Serial.printf("Logging to %s\n", name);
        return true;
      }
      return false;
    }
  }
  Serial.println("No free STG0_00.BIN..STG0_99.BIN filename.");
  return false;
}

void start_logging() {
  if (logging) {
    Serial.println("SD gate is already running.");
    return;
  }
  if (!sd_ready) {
    Serial.println("Cannot start: onboard microSD was not initialized.");
    return;
  }
  if (!choose_log_file()) {
    Serial.println("Cannot create a log file.");
    return;
  }
  ring_head = ring_tail = ring_count = 0;
  counters.dropped_records = 0;
  sd_write_failed = false;
  log_bytes = 0;
  record_sequence = 0;
  log_started_us = micros();
  sample_clock = 0;
  logging = true;
  Serial.println("10 minute microSD gate started.");
}

void stop_logging(bool completed) {
  if (!logging) return;
  logging = false;

  while (ring_count > 0 && !sd_write_failed) {
    const size_t contiguous = min(ring_count, kRingRecords - ring_tail);
    const size_t records_to_write = min(contiguous, kWriteRecords);
    const size_t bytes = records_to_write * sizeof(Stage0Record);
    if (log_file.write(reinterpret_cast<const uint8_t *>(&ring[ring_tail]),
                       bytes) != bytes) {
      sd_write_failed = true;
      break;
    }
    log_bytes += bytes;
    ring_tail = (ring_tail + records_to_write) % kRingRecords;
    ring_count -= records_to_write;
  }
  log_file.flush();
  log_file.close();

  const uint32_t elapsed_us = elapsed_since(log_started_us);
  const uint32_t rate =
      elapsed_us == 0
          ? 0
          : static_cast<uint32_t>((static_cast<uint64_t>(log_bytes) * 1000000u) /
                                  elapsed_us);
  const bool pass = completed && !sd_write_failed &&
                    counters.dropped_records == 0 &&
                    rate >= beni::stage0::kSdMinimumBytesPerSecond;
  Serial.printf("SD gate %s: %lu bytes in %.3f s, %lu B/s, dropped=%lu\n",
                pass ? "PASS" : "NOT PASSED", log_bytes,
                elapsed_us / 1000000.0, rate, counters.dropped_records);
}

void push_record() {
  if (ring_count == kRingRecords) {
    ++counters.dropped_records;
    return;
  }
  Stage0Record &record = ring[ring_head];
  memset(&record, 0, sizeof(record));
  record.magic = beni::stage0::kRecordMagic;
  record.version = beni::stage0::kRecordVersion;
  record.size = sizeof(Stage0Record);
  record.sequence = record_sequence++;
  record.t_us = micros();
  record.flags = flags_now();
  memcpy(record.raw_gyro, imu.gyro, sizeof(record.raw_gyro));
  memcpy(record.raw_accel, imu.accel, sizeof(record.raw_accel));
  record.raw_gyro_timestamp = imu.gyro_timestamp;
  record.raw_accel_timestamp = imu.accel_timestamp;
  record.can1_tx = counters.can1_tx;
  record.can1_rx = counters.can1_rx;
  record.can2_tx = counters.can2_tx;
  record.can2_rx = counters.can2_rx;
  record.can_errors = counters.can_errors;
  record.imu_events = counters.imu_events;
  record.dropped_records = counters.dropped_records;
  ring_head = (ring_head + 1) % kRingRecords;
  ++ring_count;
}

void service_sd_writer() {
  if (!logging) return;
  while (sample_clock >= beni::stage0::kSamplePeriodUs) {
    sample_clock -= beni::stage0::kSamplePeriodUs;
    push_record();
  }

  while (ring_count >= kWriteRecords && !sd_write_failed) {
    const size_t contiguous = min(ring_count, kRingRecords - ring_tail);
    if (contiguous < kWriteRecords) break;
    const size_t bytes = kWriteRecords * sizeof(Stage0Record);
    if (log_file.write(reinterpret_cast<const uint8_t *>(&ring[ring_tail]),
                       bytes) != bytes) {
      sd_write_failed = true;
      Serial.println("microSD write failed; stopping gate.");
      stop_logging(false);
      return;
    }
    log_bytes += bytes;
    ring_tail = (ring_tail + kWriteRecords) % kRingRecords;
    ring_count -= kWriteRecords;
  }

  if (elapsed_since(log_started_us) >= beni::stage0::kSdTestDurationUs) {
    stop_logging(true);
  }
}

void service_serial() {
  while (Serial.available()) {
    switch (Serial.read()) {
      case 's':
      case 'S':
        start_logging();
        break;
      case 'x':
      case 'X':
        stop_logging(false);
        break;
      case '?':
        report_status();
        break;
      default:
        break;
    }
  }
}

}  // namespace

void setup() {
  Serial.begin(beni::stage0::kSerialBaud);
  const uint32_t serial_wait_started = millis();
  while (!Serial && millis() - serial_wait_started < 3000) delay(10);

  Serial.println("Beni single-leg rig — Teensy Stage 0");
  setup_can();
  setup_imu();
  sd_ready = SD.begin(BUILTIN_SDCARD);
  Serial.println(sd_ready ? "Onboard microSD ready."
                          : "Onboard microSD not found.");
  print_help();
}

void loop() {
  service_can();
  service_imu();
  service_sd_writer();
  service_serial();
  if (status_clock >= 1000) {
    status_clock -= 1000;
    report_status();
  }
}
