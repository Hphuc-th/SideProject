# Personal Learning Track

### 2026-07-19
- Go to the english club for talking to foreigners and other learners : can hear but convey what i want smoothly 
- Complete preprocess data and loading them to the silver data. 

### 2026-07-18
- Continue to preprocess data. 
- Loading cleaned data into the next data layer (silver layer)
- Writting an essay in english 

### 2026-07-17 
- Remove unwanted space in data 
- Standalize and normalize data 
- Derived new columns from existing columns.

### 2026-07-16 
- Create a procedure to load raw data ( csv files ) into MSSS. 
- Create a procedure to check the completeness of data after loading.
- Check the time for each stage of loading to check the bottle neck

### 2026-07-13 to 2026-07-15
- Learn about the process of building a datawarehouse. 
- Learn the difference between : datawarehouse , data lake, data lakehouse , data mesh 
- Hearing to english 

## 2026-07-12
- Went to the beach.
- Watched movies in English.
- Practiced writing complete English sentences using the website: https://vi-translator.online/

## 2026-07-11
- Learned how to make suggestions.
- Worked on grammar exercises to address my weaknesses.
- Switched everything to English to maximize my exposure to the language.

## 2026-07-10
- Practiced English by listening to the news.
- Reviewed tense combinations.
- Learned how to ask questions.

## 2026-07-09
- Used Ollama to extract key information from job descriptions and benefits by converting text into JSON containing essential information such as required skills, frameworks, and specific benefits.
- Using Gemini's free-tier models by default and switching to a local Ollama model when the API quota was exceeded.
- Designed detailed prompts with JSON schema, field-level rules, and edge case handling for structured LLM output.
- Added graceful degradation: availability flags (GEMINI_AVAILABLE, QWEN_AVAILABLE, DB_AVAILABLE) so the program works without any LLM or database.

## 2026-07-08
- Extracted nested location data from jobLocation.address (street, city, region, country).
- Used Playwright to automate ITviec searches and inspect the network requests made by the website and extracted cookies from browser context for later use in automated requests.
- Handled networkidle timeout with try/except and fallback continuation.

## 2026-07-07
- Learned SQLAlchemy, including how to create and update tables and insert data.
- Used cloudscraper to bypass Cloudflare anti-bot protection on ITviec.
- Extracted job data from JSON-LD embedded in <script type="application/ld+json"> tags.
- Implemented pagination crawling: loop with page parameter, detect rel="next" link to stop, time.sleep(2) between requests for politeness.
- Cleaned HTML description/benefits with BeautifulSoup get_text(separator="\n", strip=True).

## 2026-07-06
- Went to the hospital.
- Practiced English.
- Researched coroutines and tasks in Python: https://docs.python.org/3/library/asyncio-task.html#coroutine.
- Implemented async logging with QueueHandler/QueueListener

## 2026-07-05
- Attended my friend's engagement ceremony and wedding all day.
- Rested after a long trip.

## 2026-07-04
- Listened to BBC World Service, podcasts, and watched movies in English.
- Set up Oracle.
- Solved three LeetCode problems to review PL/SQL.

## 2026-07-03
- Researched web crawling, including the crawling process and data storage.
- Reinstalled Oracle after removing old versions and unused files.
- Connected to Oracle via oracledb with context manager (with oracledb.connect() as connection).


## 2026-07-02
- Researched the technical skills required by the job market for my target positions.
- Identified my weaknesses to plan side projects that would help me improve them.

## 2026-07-01
- Defended my thesis before the examination committee.
- Relaxed after my thesis defense.
- Uploaded my CV to several job websites to search for suitable opportunities.

## 2026-06-30
- Practiced my presentation with my friend to ensure it stayed within the time limit.
- Asked my friend about any unclear points in my thesis to prepare for the defense.

## 2026-06-29
- Completed my tasks at the company before handing them over.
- Rewrote and summarized my CV to fit within two pages.
- Reviewed what I had learned to update my CV.

## 2026-06-28
- Prepared for my thesis presentation.
- Completed all documents related to my thesis.

## 2026-06-27
- Connected Python to MySQL using **SQLAlchemy**.
- Wrote basic ORM models to create tables and define columns with specific data types.
- Used a client library to send requests with headers and an access token.


## 2026-06-26
- Set up a Python virtual environment to manage backend libraries in isolation.
- Connected the backend to MongoDB using **PyMongo**.
- Configured a direct connection to a standalone MongoDB server using PyMongo and set `serverSelectionTimeoutMS` to control how long the client waits before reporting that the server is unavailable.
- Built initial Flask API endpoints to query the MongoDB database, using request parameters for filtering.
- Used Pathlib for file operation 

## General
- Practiced ETL pipeline design: Extract (crawl with cloudscraper/Playwright) → Transform (parse JSON-LD, clean HTML with BS4) → Load (MongoDB upsert + JSON file), with optional LLM enrichment step.
