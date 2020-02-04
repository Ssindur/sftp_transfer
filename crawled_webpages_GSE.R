#Group 4
#url:-https://gsejournal.biomedcentral.com
#Group Mates :Chandani Patel, Sindur Sarangi, Thitena Kebede

library(bitops)
library(RCurl)
library(XML)
library(xml2)
library(httr)
library(stringr)
library(Rcrawler)
library(rvest)
library(rlist)
library(openxlsx)

site.url = "https://gsejournal.biomedcentral.com"
main.page = read_html(site.url)
download_html(site.url,file="main.page.html")
#Extracting Articles Url
article.url=grep("articles$", LinkExtractor(site.url)[[2]], value = TRUE)
page.article.url=list()
for(i in 1:61){
  page.list[i] = paste(article.url,"?searchType=journalSearch&sort=PubDate&page=",i,sep = "")
  page.article.url=list.append(page.article.url,grep("articles/10", LinkExtractor(page.list[i])[[2]], value = TRUE))
}
#Extracting D DOI, Title, Authors, Author Affiliation, Corresponding Author, Corresponding Author Email, 
#Abstract are extracted and stored in a data frame. 
output=data.frame()
for(i in 1:length(page.article.url))
{
  for(j in 1:length(page.article.url[[i]]))
      {    download_html(page.article.url[[i]][j],file=paste(page.article.url[[i]][j],'.html',sep=""))
            page=unlist(page.article.url[[i]][j])
            html=read_html(page)
            doc = htmlParse(html, asText=TRUE)
            #Extracting Title
            Title = xpathSApply(doc, "//*[@class='ArticleTitle']", xmlValue)
            DOI = xpathSApply(doc, "//*[@class='ArticleDOI']" ,xmlValue)
            Authors = xpathSApply(doc, "//*[@class='AuthorName']", xmlValue)
                      #Authors = unlist(Authors)
            #Extracting AUthor
            AUthor_email=xpathSApply(doc, "//*[@class='EmailAuthor']",xmlGetAttr,"href")
            Auth_aff= xpathSApply(doc, "//*[@name='citation_author_institution']",xmlGetAttr,"content")
            
            #Extracting Pubdate
            PubDate = xpathSApply(doc, "//*[@class='History HistoryOnlineDate']",xmlValue )
            PubDate = gsub('Published:\\s*', '', PubDate)
            PubDate = gsub('\n', '', PubDate)
            #Extracting Abstract
            Abstract = xpathSApply(doc, "//*[@id='Abstract']",xmlValue)
            Abstract = gsub('\n', '', Abstract)
            Abstract = gsub('\\sBackground\\s*', 'Background:', Abstract)
            Abstract = gsub('\\sResults\\s*', 'Results:', Abstract)
            Abstract = gsub('\\sConclusions\\s*', 'Conclusions:', Abstract)
            Abstract =trimws(Abstract,which="both")
            #COncatenating all fields into one
            extract_row <- data.frame( DOI = paste(DOI,collapse = ','),
                                       Title = paste(Title,collapse = ','),
                                      Authors = paste(Authors, collapse =','),
                                      Corresponding_Author = paste(Authors[1],collaspse=','),
                                      Corresponding_Author_Email = paste(AUthor_email,collapse = ','),
                                      Author_Affiliations=paste(Auth_aff, collapse =','),
                                      Published_Date = PubDate, 
                                      Abstract = paste(Abstract,collapse= ','),
                                      Keywords = "NA",
                                      FullText = "NA")
            #Appending the extracted row of each article to output dataframe
            output = rbind(output,  extract_row)
  }
}
# Writting the output dataframe 
write.table(output,file="Genetics_Selection_Evolution.txt",sep="\t",row.names=FALSE)
#reading a text file
reading.output=read.table("Genetics_Selection_Evolution.txt", header = TRUE, sep = "\t")
#writting summary to excel sheet
write.xlsx(reading.output,"GSE_summary_of_fileds.xlsx",sheetName = "Sheet1",col.names = TRUE,keepNA=TRUE)
