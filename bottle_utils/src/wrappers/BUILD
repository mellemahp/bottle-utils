load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "wrappers_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        "//:templating",
        requirement("structlog"),
        requirement("bottle"),
    ],
)
