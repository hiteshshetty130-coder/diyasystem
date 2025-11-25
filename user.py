#importing modules
import requests
import pandas as pd
from pandas import DataFrame

def main():
    retry = 3
    for attempt in range(1,retry+1):    #run the loop to try to fetch the data till specified
        #try except for error handling mechanism
        try:
            url = "https://api.slingacademy.com/v1/sample-data/files/employees.json"
            response = requests.get(url,timeout=3)

            if response.status_code == 200:  #if url successfully returns the data
                data = response.json()
                df = DataFrame(data)

                #creating the csv file for testing the file type later
                file_path = "data.csv"
                df.to_csv(file_path, index=False)

                pd.set_option('display.max_columns', None)
                df=df.rename(columns = {"id":"Employee ID", "first_name":"First Name",
                                    "last_name":"Last Name", "email":"Email",
                                    "job_title":"Job Title", "phone":"Phone Number"})

                #function to get values for designation
                def designation_values(experience):
                    if experience < 3:
                        return "System Engineer"
                    elif experience >= 3 and experience <= 5:
                        return "Data Engineer"
                    elif experience > 5 and experience < 10:
                        return "Senior Data Engineer"
                    else:
                        return "Lead"

                df["Designation"] = df["years_of_experience"].apply(designation_values) #apply the function returned value

                df["Full Name"] = df["First Name"] + ' ' + df["Last Name"] # find values for new column full name

                #lambda function to check if the number is invalid
                df["Phone Number"] = df["Phone Number"].apply(lambda number : "Invalid Number" if "X" in str(number).upper() else number)


                df = df.astype({"First Name":"string", "Last Name":"string", "Email":"string",
                                "Phone Number":"string", "gender":"string", "Job Title":"string",     #specify data type of all columns
                                "department":"string", "Designation":"string", "Full Name":"string"})

                #final structure of the data Frame
                df = df[["Employee ID", "Full Name", "First Name", "Last Name", "Email",
                         "Job Title", "Phone Number","years_of_experience"]]

                return df

            else:
                print("request failed", response.status_code) #if api does not return data
                break



        except requests.exceptions.Timeout: #exception for request timed out
            print("ERROR! Sorry Request Timed Out!")

        except requests.exceptions.ConnectionError: # internet connectivity problem
            print("ERROR! Please check the internet connection!")

        except requests.exceptions.RequestException as e: #other error if caught
            print("Other ERROR!",e)

        #if attempt reaches maximum tries then loop ends
        if attempt == retry:
            print("SORRY MAXIMUM ATTEMPTS LIMIT REACHED")

        else:
            print("RETRYING......")

if __name__ == "__main__":
    main()

