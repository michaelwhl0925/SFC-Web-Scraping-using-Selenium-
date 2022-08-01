# SFC Web Scraping using Selenium

Here is one of the Python programming projects I have done in my previous internship.

As the required website "https://apps.sfc.hk/publicregWeb/searchByRa?locale=en" is dynamically loaded with javascript, it provides results based on users' actions.
Hence, the Python Selenium module is used to "mimic" the human actions and, as a result, successfully extract all the required information on the site.

In this program, I will attempt to extract all companies' info (CE Ref Num, Name, Chinese Name, Address, With Active Record) 
under the "Type 9: Asset Management, Corporation" criteria.

Difficulties encountered during coding:
1. Sometimes the website blocks me from scraping. Hence, I need to intentionally suspend the program from running by using "time.sleep()"
2. I was looking for any API links which could scrape the information much faster than using Selenium (which is slow), yet I could not find any.
3. I had also looked for python vectorization to turn all WebElements to text in the dataframe at once. However, the method seemed not feasible and brutal loops were used which slowed down the process.

P.S. Not attempt to have any conflicts of interests :)
