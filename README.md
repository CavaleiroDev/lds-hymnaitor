# LDS HYMNAITOR
A simple web scraper that extracts hymn data of the LDS new hymnbook and exports it into .json files

Also includes code in Typst that uses those .json files to generate a pdf with each hymn lyrics

Data is also included here (which probably isnt a good idea) for hymns in Portuguese

# SPAGHETTI CODE WARNING
**This is a very simple project** that was made for me to have a pdf with every new hymn without needing to make it manually. Im sharing it here in hopes that it may be helpfull for someone else's project

With that being said, there is quite a few things i had to implement manually hymn after hymn:
- specific page breaks so that the PDF could be printed and used without page leaking to other sheets (defined inside Typst code)
- which hymns are displayed in 1 or 2 columns (defined in 'columns.json')
- blacklisted text to filter unnecessary credits info

The code here is NOT optimized and if you wanna use it you might have to change it a bit. Specially if you want to generate data in English. You shold be able to just change the URL but it might break some small things
