from src.abstract import Paste


def test_required_fields_to_object():
    """
    test_required_fields_to_object

    validate that all required fields in a Paste object
    are populated

    """
    required_keys = ["id", "content", "created_time_epoch"]
    valid_paste = Paste(content="test")
    to_object_dict = valid_paste.dict()
    for k in required_keys:
        assert to_object_dict[k] is not None
