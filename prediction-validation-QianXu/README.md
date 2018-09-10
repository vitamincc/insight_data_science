What is in package:

The directory structure for this repo should look like:
```
.
├── README.md
├── run.sh
├── src
│   └── prediction-validation.py
├── input
│   ├── actual.txt
│   ├── predicted.txt
│   └── window.txt
├── output
│   └── comparison.txt
└── insight_testsuite
    ├── run_tests.sh
    └── tests
        ├── test_1
        │   ├── input
        │   │   ├── actual.txt
        │   │   ├── predicted.txt
        │   │   └── window.txt
        │   └── output
        │       └── comparison.txt
        │
        ├── my_test_1
        │   ├── input
        │   │   └── actual.txt
        │   │   
        │   │   
        │   └── output
        │       └── comparison.txt
        │
        ├── my_test_2
        │   ├── input
        │   │   ├── actual.txt
        │   │   ├── predicted.txt
        │   │   └── window.txt
        │   └── output
        │       └── comparison.txt
        │
        ├── my_test_3
        │   ├── input
        │   │   ├── actual.txt
        │   │   ├── predicted.txt
        │   │   └── window.txt
        │   └── output
        │       └── comparison.txt
        │
        ├── my_test_4
        │   ├── input
        │   │   ├── actual.txt
        │   │   ├── predicted.txt
        │   │   └── window.txt
        │   └── output
        │       └── comparison.txt
        │
        └── my_test_5
            ├── input
            │   ├── actual.txt
            │   ├── predicted.txt
            │   └── window.txt
            └── output
                └── comparison.txt     
```   

What dependencies are required:
```
The codes were done in python 3.6.
Packages sys, pandas, numpy, os, decimal and collections are used in this program, 
in which pandas and numpy were installed by myself.
```

How to execute:
```
To execute the input under the root folder, run command 
	./run.sh
To execute the tests, run command 
	./run_tests.sh
```

What approach is used to implement:
```
1. Read files from input, and split actual and predicted data to three columns "time","stock" and "price".
2. Inner joined reformed actual data and predicted data, and calculated price error of the stocks between actual and predicted data.
3. Calculated sum of price error and count of stocks which are grouped by matched hours
4. Calculated avarage error of each time window
```

What test cases are included:
```
1. my_test_1: Check if files exist.
   Here window file does not exist, output error message in comparison.txt to clarify the file does not exist.

2. my_test_2: Check average error of un-matched hours 
   When there is a gap in predicted time series and maximum of predicted time is much smaller than that of actual time,
   the average error of un-matched hours will be output as NA.
   Here hours in predicted.txt are from 1~3 and 8~10, hours in acutal.txt are from 1~1440.
   
3. my_test_3: Check if files are null.
   Here no data is in predicted file, then output error message "No data in prediction file." in comparison.txt,
   and then break the program.
   
4. my_test_4: Check window size.
   Here the window size is 1445, larger than maximum of actual time 1440, then output error message
   "Window size is out of index, no result will be output." in comparison.txt, and break the program.

5. my_test_5: Check window size.
   Here the window size is 0, then output error message "Window size is negative or defined as 0, 
   no result will be output." in comparison.txt, and break the program.
  
6. test_1: official test case provided by Insight. 
   There is +/- 0.1 difference of some data between my results and official results.
```



