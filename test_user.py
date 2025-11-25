#importing all the modules and files
import unittest
from unittest.mock import patch,Mock
from user import main
import pandas as pd

class TestDataExtraction(unittest.TestCase):
    #Test Case 1:Validate json file download
    @patch("user.requests.get")#creating a mock request
    def test_main1(self,mock_get):

        mock_data=[{"id":1, "first_name":"Hitesh",
                                    "last_name":"Kumar", "email":"HiteshKumar@gmail.com",
                                    "job_title":"Web Developer", "phone":"9876524132","years_of_experience":5,
                    "department":"It Manager","gender":"Male"}]

        mock_response=Mock() #mock object creation
        mock_response.status_code=200
        mock_response.json.return_value=mock_data #object gets mock data in json format
        mock_get.return_value=mock_response

        df=main() #return value from main function

        #checks in df returned as some value
        self.assertIsNotNone(df)


    #Test Case 2:Verify json file Extraction
    @patch("user.requests.get")
    def test_main2(self,mock_get):
        mock_data=[{"id":1, "first_name":"Hitesh",
                                    "last_name":"Kumar", "email":"HiteshKumar@gmail.com",
                                    "job_title":"Web Developer", "phone":"9876524132","years_of_experience":5,
                    "department":"It Manager","gender":"Male"}]
        mock_response=Mock()
        mock_response.status_code=200
        mock_response.json.return_value=mock_data
        mock_get.return_value=mock_response

        df=main()
        # checks if df is a data frame and checks if number of rows are equal
        self.assertIsInstance(df,pd.DataFrame)
        self.assertEqual(len(df),len(mock_data))


    #Test Case 3: validate file type and format
    @patch("user.requests.get")
    def test_main3(self,mock_get):
        mock_data = [{"id": 1, "first_name": "Hitesh",
                      "last_name": "Kumar", "email": "HiteshKumar@gmail.com",
                      "job_title": "Web Developer", "phone": "9876524132", "years_of_experience": 5,
                      "department": "It Manager", "gender": "Male"}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        file_path=r"data.csv"
        try:
            df = pd.read_csv(file_path)           #read a csv file which specifies file type
        except Exception as e:
            self.fail(f"cannot read file {e}")


    #Test case 4: Validate the data Structure
    @patch("user.requests.get")
    def test_main4(self,mock_get):
        mock_data = [{"id": 1, "first_name": "Hitesh",
                      "last_name": "Kumar", "email": "HiteshKumar@gmail.com",
                      "job_title": "Web Developer", "phone": "9876524132", "years_of_experience": 5,
                      "department": "It Manager", "gender": "Male"}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        df=main()

        #checks the structure of Data Frame
        expected_columns = ["Employee ID", "Full Name", "First Name", "Last Name", "Email", "Job Title", "Phone Number",
                            "years_of_experience"]
        for cols in expected_columns:
            self.assertIn(cols, df.columns)

    #Test Case 5: Handle Missing and Invalid Data
    @patch("user.requests.get")
    def test_main5(self,mock_get):
        mock_data = [{"id": 1, "first_name": "Hitesh",
                      "last_name": "Kumar", "email": "HiteshKumar@gmail.com",
                      "job_title": "Web Developer", "phone": "98765X4132", "years_of_experience": 5,
                      "department": "It Manager", "gender": "Male"}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        df = main()

        #checks if first name and last name columns has values
        self.assertFalse(df["First Name"].isnull().any())
        self.assertFalse(df["Last Name"].isnull().any())

        #checks if email is valid
        for email in df["Email"]:
            self.assertIn("@",email)

        #chceks if invalid number is checked correctly or not
        self.assertEqual(df.iloc[0]["Phone Number"],"Invalid Number")


if __name__=="__main__":
    unittest.main()

