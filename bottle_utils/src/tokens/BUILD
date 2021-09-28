load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "tokens_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        "//:monitoring",
        requirement("structlog"),
        requirement("bottle"),
    ],
)
