-- SELECT * FROM allData;
-- UPDATE users SET last_view = 940704000 WHERE email = 'utsavmaan28@gmail.com'
-- DELETE FROM allData;
SELECT * FROM allData;
-- SELECT * FROM applyQueue;
-- SELECT * FROM resumeList;
SELECT * FROM users;


-- INSERT INTO allData (id, title, location, company, description, dateUpdated) 
--             VALUES ('ID', 'title', 'locatin', 'company', 'description,', 70707070);

-- DELETE FROM resumeList;
-- DROP TABLE resumeList;



-- Processing Jobs:   6%|█████████▍                                                                                                                                                                 | 7/127 [01:04<15:38,  7.82s/it]2024-08-10 18:07:30,746 - ERROR - Error in adding data for jobID: 7545ba36-d78e-4b70-8808-b274e1abf85a
-- Traceback (most recent call last):
--   File "C:\Users\utsav\Desktop\Dice-JobScraping\dataHandling.py", line 24, in addNewJobSQL
--     conn = odbc.connect(connectionString)
--   File "C:\Users\utsav\AppData\Local\Programs\Python\Python38\lib\site-packages\pypyodbc.py", line 2454, in __init__
--     self.connect(connectString, autocommit, ansi, timeout, unicode_results, readonly)
--   File "C:\Users\utsav\AppData\Local\Programs\Python\Python38\lib\site-packages\pypyodbc.py", line 2507, in connect
--     check_success(self, ret)
--   File "C:\Users\utsav\AppData\Local\Programs\Python\Python38\lib\site-packages\pypyodbc.py", line 1009, in check_success
--     ctrl_err(SQL_HANDLE_DBC, ODBC_obj.dbc_h, ret, ODBC_obj.ansi)
--   File "C:\Users\utsav\AppData\Local\Programs\Python\Python38\lib\site-packages\pypyodbc.py", line 987, in ctrl_err
--     raise DatabaseError(state,err_text)
-- pypyodbc.DatabaseError: ('08001', '[08001] [Microsoft][ODBC Driver 17 for SQL Server]TCP Provider: The wait operation timed out.\r\n')