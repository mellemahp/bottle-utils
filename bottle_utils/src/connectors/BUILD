load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "connectors_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        requirement("redis"),
        requirement("structlog"),
        requirement("redislite"),
        requirement("peewee"),
    ],
)
