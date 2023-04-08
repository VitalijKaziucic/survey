from survey import Survey


if __name__ == "__main__":
    new_survey = Survey([f"Project {i}" for i in range(1, 16)], ["Vitalijus", "Rapolas", "Renata"])
    new_survey.run_app()