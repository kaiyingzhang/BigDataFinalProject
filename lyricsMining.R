devtools::install_github("mjockers/syuzhet")
install.packages("textcat")

library(ggplot2)
library(tm)
library(wordcloud)
library(syuzhet)
library(SnowballC)
library(textcat)


texts <-file("/Users/PP/Desktop/vs/basicData-A~Z/song_labels_R.txt","r")##texts is the whole file
outfile <- file("/Users/PP/Desktop/vs/Output_R/songR_labels_R.txt", "w") 
line<-readLines(texts,n=1)
##paste(line)
while( length(line) != 0) {
  line1 <- strsplit(line,",")
  LyricsLine <- line1[[1]][3]##find the lyrics part
  ArtistLine <- line1[[1]][1]
  SongNameLine <- line1[[1]][2]
  
  
  if((!is.na(textcat(LyricsLine)))&&(textcat(LyricsLine) == 'english')&&(length(LyricsLine)>=1)){
    ##print(LyricsLine)
    
    docs <- Corpus(VectorSource(LyricsLine))##read the text 
    
    
    docs <- tm_map(docs, removePunctuation)
    docs <- tm_map(docs, removeNumbers)
    docs <- tm_map(docs, tolower)
    docs <- tm_map(docs, removeWords, stopwords("english"))
    ## docs <- tm_map(docs, removeWords, c("black", "bones")) 
    
    docs <- tm_map(docs, stemDocument)
    
    docs <- tm_map(docs, stripWhitespace)
    
    docs <- tm_map(docs, PlainTextDocument)
    
    ######build TDM
    
    dtm <- TermDocumentMatrix(docs)
    mat <- as.matrix(dtm)
    v <- sort(rowSums(mat),decreasing = TRUE)
    
    
    d <- data.frame(word = names(v),freq = v)
    ##head (d,10)##get top 10 frequent words
    topWords <- as.character(head(d,10)$word)##get the first row
    
    #
    #paste0(topWords)
    ##while(length(topWords)>1){
    Sentiment <- get_nrc_sentiment(LyricsLine)
    text <- cbind(LyricsLine,Sentiment)
    
    TotalSentiment <- data.frame(colSums(text[,c(2:11)]))
    names(TotalSentiment) <- "count"
    TotalSentiment <- cbind("sentiment" = rownames(TotalSentiment),TotalSentiment)
    rownames(TotalSentiment) <- NULL
    
    ##ggplot(data = TotalSentiment, aes(x = sentiment, y = count))+
    ##geom_bar(aes(fill = sentiment), stat = "identity")+
    ##theme(legend.position = "none") +
    ##xlab("Sentiment") + ylab("Total Count") + ggtitle("Total Sentiment Score")
    sentiText <- text[,c(2:11)]
    
    DescSentiment <- TotalSentiment[order(TotalSentiment[,2],decreasing=T),]
    topSentiment <- head(DescSentiment,5)[,1]
    ##print(topSentiment)
    
    ##score
    totolScore <- sentiText[,1]+sentiText[,2]+sentiText[,3]+sentiText[,4]+sentiText[,5]+sentiText[,6]+sentiText[,7]+sentiText[,8]+sentiText[,9]+sentiText[,10]
    positiveScore <- sentiText[,2]+sentiText[,5]+sentiText[,7]+sentiText[,8]+sentiText[,10]
    
    SentiScore<- floor((positiveScore/totolScore*10))
    
    joySentiment <- sentiText[,2]+sentiText[,5]+sentiText[,7]+sentiText[,8]
    joyScore<-  floor(joySentiment/totolScore*10)
    
    sorrowSentiment <- sentiText[,6]+sentiText[,4]
    sorrowScore<-  floor(sorrowSentiment/totolScore*10)
    
    surpriseScore <-  floor(sentiText[,7]/totolScore*10)
    
    angryScore <-  floor(sentiText[,1]/totolScore*10)
    
    ######
    
    totalResult <- c(paste0(ArtistLine),sep=",",paste0(SongNameLine),sep=",",
                     SentiScore,sep=",",
                     joyScore,sep=",",sorrowScore,sep=",",angryScore,sep=",",surpriseScore,sep=",",
                     paste0(topWords),sep="\n")
    ##paste0(totalResult)
    
    ##write.table(paste(totalResult, sep=" ", collapse=", "), "/Users/kein/Desktop/tryResult/Rdata1.txt", sep="\t")
    cat(totalResult,file=outfile) 
    line<-readLines(texts,n=1)
  }else{
    line<-readLines(texts,n=1)
    
  }
  
  
}
print ("Done")
##outfile <- file("/Users/PP/Desktop/vs/basicData-A~J/Done.txt", "w") 



