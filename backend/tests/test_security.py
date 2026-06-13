from app.core.security import hash_api_key, verify_api_key


def test_hash_api_key_is_deterministic_sha256() -> None:
    api_key_hash = hash_api_key("demo-key")

    assert api_key_hash == (
        "c48a01f49fd0f2cc404bc3cbbc80e91457a3d41bb429a695243de4c61794155c"
    )
    assert verify_api_key("demo-key", api_key_hash)
    assert not verify_api_key("wrong-key", api_key_hash)
