from your_package_name.main import main


def test_import_and_run(capsys):
    main()
    captured = capsys.readouterr()
    assert "Python PyPI starter is ready." in captured.out
