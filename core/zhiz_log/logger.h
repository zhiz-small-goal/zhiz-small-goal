// core/zhiz_log/logger.h
#pragma once
#include <string_view>

namespace zhiz::log {
enum class Level { Info, Warn, Error };

void init(std::string_view dir);
void write(Level lv, std::string_view msg);
void info(std::string_view msg);
void error(std::string_view msg);
} // namespace zhiz::log
