#pragma once
#include <asm/unistd.h>
#include <linux/hw_breakpoint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <cerrno>
#include <chrono>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <vector>

void enable_perf_event(int fd) {
  if (ioctl(fd, PERF_EVENT_IOC_ENABLE, 0) == -1) {
    std::cerr << "Error enabling perf event: " << strerror(errno) << std::endl;
  }
}
void disable_perf_event(int fd) {
  if (ioctl(fd, PERF_EVENT_IOC_DISABLE, 0) == -1) {
    std::cerr << "Error disabling perf event: " << strerror(errno) << std::endl;
  }
}
int perf_event_open(struct perf_event_attr* hw_event, pid_t pid, int cpu, int group_fd, unsigned long flags) {
  return syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
}
int setup_perf_event(int perf_no) {
  perf_event_attr pe;
  memset(&pe, 0, sizeof(struct perf_event_attr));
  pe.size = sizeof(struct perf_event_attr);

  // 설정하는 이벤트에 따라 다른 성능 카운터를 선택
  if (perf_no == 0) {
    pe.type = PERF_TYPE_HW_CACHE;
    pe.config = (PERF_COUNT_HW_CACHE_LL) |
                (PERF_COUNT_HW_CACHE_OP_READ << 8) |
                (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
  } else if (perf_no == 1) {
    pe.type = PERF_TYPE_HW_CACHE;
    pe.config = (PERF_COUNT_HW_CACHE_DTLB) |
                (PERF_COUNT_HW_CACHE_OP_READ << 8) |
                (PERF_COUNT_HW_CACHE_RESULT_MISS << 16);
  } else if (perf_no == 2) {
    pe.type = PERF_TYPE_HARDWARE;
    pe.config = PERF_COUNT_HW_BRANCH_MISSES;
  } else if (perf_no == 3) {
    pe.type = PERF_TYPE_HARDWARE;
    pe.config = PERF_COUNT_HW_INSTRUCTIONS;
  }

  // 성능 카운터를 열고, 파일 디스크립터 반환
  int fd = perf_event_open(&pe, 0, -1, -1, 0);
  if (fd == -1) {
    std::cerr << "Error opening perf event: " << strerror(errno) << std::endl;
  }
  return fd;
}

long long close_perf_event(int fd) {
  long long results = 0;
  if (read(fd, &results, sizeof(long long)) == -1) {
    std::cerr << "Error reading perf event: " << strerror(errno) << std::endl;
    close(fd);
  }
  return results;
}

