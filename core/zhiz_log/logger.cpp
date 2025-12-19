// core/zhiz_log/logger.cpp
#include "core/zhiz_log/logger.h"

#include <chrono>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <sstream>
#include <string>
#include <iostream>
#include <ctime>
#include <iomanip>
#include <string_view>

namespace zhiz::log {

namespace {
  std::mutex g_mu;
  std::filesystem::path g_dir;
  std::filesystem::path g_file;   // g_dir / "zhiz_tool.log"
  std::ofstream g_out;
  bool g_inited = false;

  // TODO(你来实现): 把 Level 映射为 "INFO"/"ERROR"/...
  const char* to_text(Level lv) {
    switch (lv) {
      case Level::Info:  return "INFO";
      case Level::Warn:  return "WARN";
      case Level::Error: return "ERROR";
      default:           return "UNKNOWN";
    }
  }

  // TODO(你来实现): 生成时间戳字符串，例如 "2025-12-18 20:15:03.123"
  std::string now_text() {
    // 提示：用 std::chrono::system_clock::now()
    using clock = std::chrono::system_clock;
    const auto now = clock::now();
    const std::time_t t = clock::to_time_t(now);

    std::tm tm{};
    #ifdef _WIN32
    localtime_s(&tm, &t);
    #else
    localtime_r(&t, &tm);
    #endif

    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
    return oss.str();

  }

  void open_stream_if_needed() {
    if (g_out.is_open()) return;
    // 目录不一定存在，确保创建
    std::error_code ec;
    std::filesystem::create_directories(g_dir, ec);
    // 打开为追加写
    g_out.open(g_file, std::ios::app);
  }

  void write_line(Level lv, std::string_view msg) {
    // 先在锁外拼整行，降低锁持有时间
    std::ostringstream oss;
    oss << now_text() << " [" << to_text(lv) << "] " << msg << "\n";
    const std::string line = oss.str();

    std::lock_guard<std::mutex> lk(g_mu);

    // 若未 init，给一个默认目录（避免调用方必须记得 init）
    if (!g_inited) {
      g_dir = "zhiz_logs";
      g_file = g_dir / "zhiz_tool.log";
      g_inited = true;
    }

    open_stream_if_needed();
    if (g_out.is_open()) {
      g_out << line;
      // v0：每行 flush，保证崩溃时也尽量有日志；后续可改为批量 flush
      g_out.flush();
    } else {
      // 降级：至少能看到信息
      std::cerr << line;
    }
  }
} // namespace

void init(std::string_view dir) {
  std::lock_guard<std::mutex> lk(g_mu);
  g_dir = std::filesystem::path(dir);
  g_file = g_dir / "zhiz_tool.log";
  g_inited = true;

  // 重新打开（覆盖旧句柄）
  if (g_out.is_open()) g_out.close();
  open_stream_if_needed();
}

void write(Level lv, std::string_view msg) { write_line(lv, msg); }
void info(std::string_view msg) { write_line(Level::Info, msg); }
void error(std::string_view msg) { write_line(Level::Error, msg); }

} // namespace zhiz::log
