def test():
    return (
        "Không thể tải audio từ URL này. "
        "Hãy thử link trực tiếp hoặc kiểm tra lại URL.",
        (None, None)
    )

info, result_audio = test()
print("Success!")
