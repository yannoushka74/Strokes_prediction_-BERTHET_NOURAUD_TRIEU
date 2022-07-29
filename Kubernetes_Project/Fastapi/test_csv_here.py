from os.path import exists
from datetime import date


def is_csv_here(filename):
    file_exists = exists(filename)
    test_date = date.today()
    if file_exists == True:
        test_status = "SUCCESS"
    else:
        test_status = "FAILURE"

    output = '''
        =================================
            CHECK IF CSV IS AVAILABLE
        =================================
        test date = {test_date}
        tested file = {filename}

        expected result = True
        actual restult = {file_exists}

        ==>  {test_status}

        '''
    print(output.format(filename=filename, file_exists=file_exists,
          test_status=test_status, test_date=test_date))
    # Impression dans le fichier de log
    if exists("api_test.log") == True:
        with open("api_test.log", 'a')as file:
            file.write(output.format(
                filename=filename,
                file_exists=file_exists,
                test_status=test_status,
                test_date=test_date
            ))
