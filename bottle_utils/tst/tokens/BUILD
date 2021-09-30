load("@pip_deps//:requirements.bzl", "requirement")

py_test(
    name = "session_test",
    srcs = ["session_test.py"],
    deps = [
        "//:tokens",
        requirement("pytest"),
    ],
)

py_test(
    name = "csrf_test",
    srcs = ["csrf_test.py"],
    deps = [
        "//:tokens",
        requirement("pytest"),
    ],
)

py_test(
    name = "token_manager_test",
    srcs = ["token_manager_test.py"],
    deps = [
        "//:tokens",
        requirement("pytest"),
    ],
)

py_test(
    name = "verification_test",
    srcs = ["verification_test.py"],
    deps = [
        "//:tokens",
        requirement("pytest"),
    ],
)
