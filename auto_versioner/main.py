from auto_versioner import current_working_path, Controller


def run():
    auto_versioner = Controller(current_working_path)
    auto_versioner.run()
