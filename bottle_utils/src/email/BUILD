load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "email_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        "//:monitoring",
    ],
)
