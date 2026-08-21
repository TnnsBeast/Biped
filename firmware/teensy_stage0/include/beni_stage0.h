#pragma once

#include <Arduino.h>

namespace beni::stage0 {

constexpr uint32_t kSerialBaud = 115200;
constexpr uint32_t kCanBaud = 500000;
constexpr uint32_t kSamplePeriodUs = 1000;
constexpr uint32_t kImuReportPeriodUs = 1000;
constexpr uint32_t kSdTestDurationUs = 600000000;
constexpr uint32_t kSdMinimumBytesPerSecond = 240000;
constexpr uint32_t kRecordMagic = 0x30494E42;  // "BNI0" in little endian.
constexpr uint16_t kRecordVersion = 1;

// Teensy 4.1 primary SPI pins are MOSI 11, MISO 12 and SCK 13. These three
// control pins are intentionally centralized here; verify them against the
// physical harness before connecting the BNO085.
constexpr uint8_t kBnoCsPin = 10;
constexpr uint8_t kBnoIntPin = 9;
constexpr int8_t kBnoResetPin = 8;

constexpr uint32_t kCan1TestId = 0x6A1;
constexpr uint32_t kCan2TestId = 0x6A2;

enum StatusFlag : uint32_t {
  kCan1LoopbackOk = 1u << 0,
  kCan2LoopbackOk = 1u << 1,
  kSdActive = 1u << 2,
  kImuPresent = 1u << 3,
  kImuRawAccelSeen = 1u << 4,
  kImuRawGyroSeen = 1u << 5,
};

#pragma pack(push, 1)
struct Stage0Record {
  uint32_t magic;
  uint16_t version;
  uint16_t size;
  uint32_t sequence;
  uint32_t t_us;
  uint32_t flags;
  int16_t raw_gyro[3];
  int16_t raw_accel[3];
  uint32_t raw_gyro_timestamp;
  uint32_t raw_accel_timestamp;
  uint32_t can1_tx;
  uint32_t can1_rx;
  uint32_t can2_tx;
  uint32_t can2_rx;
  uint32_t can_errors;
  uint32_t imu_events;
  uint32_t dropped_records;
  uint8_t reserved[188];
};
#pragma pack(pop)

static_assert(sizeof(Stage0Record) == 256,
              "Stage 0 record must remain 256 bytes (256 kB/s at 1 kHz)");

}  // namespace beni::stage0
