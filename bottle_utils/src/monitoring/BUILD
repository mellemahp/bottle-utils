load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "monitoring_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        requirement("structlog"),
        requirement("prometheus-client"),
    ],
)
