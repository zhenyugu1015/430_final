library(data.table)
library(keras)
library(dplyr)
library(tidyr)
library(reshape2)

myPred_2 <- function(path1, path2, path3, path4, data_path){
  pathes <- list(path1, path2, path3, path4)
  e <- new.env()
  load(data_path, envir = e)
  dat_processed <- list()
  for (i in 1:4) {
    dataname <- pathes[[i]]
    raw1 <- fread(dataname)
    raw1$s <- raw1$Timestamp%/%1000
    raw1$h <- floor(raw1$s/10000)
    raw1$m <- floor((raw1$s-raw1$h*10000)/100)
    raw1$s <- (raw1$s-raw1$h*10000-raw1$m*100)
    Price <- as.data.frame(apply(raw1[, c(4:13)], 2, colsplit, pattern = "x", names = c("Price", "right")))
    Volume <- as.data.frame(apply(Price[,seq(2, 20, 2)], 2, colsplit, pattern = "[(]", names = c("Volume", "Order")))
    Orders = as.data.frame(apply(Volume[,seq(2, 20, 2)], 2, extract_numeric))
    Volume <- Volume[,seq(1, 20, 2)]
    Price <- Price[,seq(1, 20, 2)]
    P.V <- cbind(Price, Volume)
    data <- raw1[, -c(4:13)]
    price.mat <- as.matrix(Price)
    volume.mat <- as.matrix(Volume)
    mat.pv <- as.data.frame(price.mat * volume.mat)
    names(mat.pv) <- paste0(names(mat.pv), ".weighted")
    data <- cbind(data, P.V, mat.pv)
    data <- cbind(data, Orders)
    
    me.price <- aggregate(data.frame(data[, 7:16]), by=list(data$s, data$m, data$h, data$Side), mean, na.rm = TRUE)
    names(me.price)[1:4] <- c("s", "m", "h", "Side")
    me.price.buy <- me.price[me.price$Side == "BUY",]
    me.price.sell <- me.price[me.price$Side == "SELL",]
    me.price.merge <- merge(me.price.buy, me.price.sell, by=c("s", "m", "h"), all = TRUE)
    name <- names(me.price.merge)
    names(me.price.merge)[-c(1:3)] <- c(gsub("x", "me.Buy", name[c(4:14)]), gsub("y", "me.Sell", name[c(15:25)]))
    
    open.price <- aggregate(data[, 7:16], by=list(data$s, data$m, data$h, data$Side), first)
    names(open.price)[1:4] <- c("s", "m", "h", "Side")
    open.price.buy <- open.price[open.price$Side == "BUY",]
    open.price.sell <- open.price[open.price$Side == "SELL",]
    open.price.merge <- merge(open.price.buy, open.price.sell, by=c("s","m", "h"), all = TRUE)
    name <- names(open.price.merge)
    names(open.price.merge)[-c(1:3)] <- c(gsub("x", "open.Buy", name[c(4:14)]), gsub("y", "open.Sell", name[c(15:25)]))
    
    close.price <- aggregate(data[, 7:16], by=list(data$s, data$m, data$h, data$Side), last)
    names(close.price)[1:4] <- c("s", "m", "h", "Side")
    close.price.buy <- close.price[close.price$Side == "BUY",]
    close.price.sell <- close.price[close.price$Side == "SELL",]
    close.price.merge <- merge(close.price.buy, close.price.sell, by=c("s","m", "h"), all = TRUE)
    name <- names(close.price.merge)
    names(close.price.merge)[-c(1:3)] <- c(gsub("x", "close.Buy", name[c(4:14)]), gsub("y", "close.Sell", name[c(15:25)]))
    
    sum.vol <- aggregate(data[, 17:26], by=list(data$s, data$m, data$h, data$Side), sum, na.rm = TRUE)
    names(sum.vol) <- c("s", "m", "h", "Side", "Level1.Volume","Level2.Volume","Level3.Volume",
                        "Level4.Volume","Level5.Volume","Level6.Volume","Level7.Volume",
                        "Level8.Volume","Level9.Volume","Level10.Volume")
    sum.vol.buy <- sum.vol[sum.vol$Side == "BUY",]
    sum.vol.sell <- sum.vol[sum.vol$Side == "SELL",]
    sum.vol.merge <- merge(sum.vol.buy, sum.vol.sell, by=c("s","m", "h"), all = TRUE)
    name <- names(sum.vol.merge)
    names(sum.vol.merge)[-c(1:3)] <- c(gsub("x", "Buy", name[c(4:14)]), gsub("y", "Sell", name[c(15:25)]))
    
    sum.ord <- aggregate(data[, 37:46], by=list(data$s, data$m, data$h, data$Side), sum, na.rm = TRUE)
    names(sum.ord) <- c("s", "m", "h", "Side", "Level1.Order","Level2.Order","Level3.Order",
                        "Level4.Order","Level5.Order","Level6.Order","Level7.Order",
                        "Level8.Order","Level9.Order","Level10.Order")
    sum.ord.buy <- sum.ord[sum.ord$Side == "BUY",]
    sum.ord.sell <- sum.ord[sum.ord$Side == "SELL",]
    sum.ord.merge <- merge(sum.ord.buy, sum.ord.sell, by=c("s","m", "h"), all = TRUE)
    name <- names(sum.ord.merge)
    names(sum.ord.merge)[-c(1:3)] <- c(gsub("x", "Buy", name[c(4:14)]), gsub("y", "Sell", name[c(15:25)]))
    
    wm.price <- aggregate(data.frame(data[, 27:36]), by=list(data$s, data$m, data$h, data$Side), sum, na.rm = TRUE)
    wm.price[,5:14] <- wm.price[,5:14]/sum.vol[,5:14]
    names(wm.price)[1:4] <- c("s", "m", "h", "Side")
    wm.price.buy <- wm.price[wm.price$Side == "BUY",]
    wm.price.sell <- wm.price[wm.price$Side == "SELL",]
    wm.price.merge <- merge(wm.price.buy, wm.price.sell, by=c("s","m", "h"), all = TRUE)
    name <- names(wm.price.merge)
    names(wm.price.merge)[-c(1:3)] <- c(gsub("x", "Buy", name[c(4:14)]), gsub("y", "Sell", name[c(15:25)]))
    
    P.V.merge <- cbind(open.price.merge, me.price.merge, sum.vol.merge, wm.price.merge, close.price.merge, sum.ord.merge)
    P.V.merge <- P.V.merge[order(P.V.merge$h, P.V.merge$m, P.V.merge$s),]
    dat_processed[[i]] <- P.V.merge[, -c(4, 15, 26:29, 40, 51:54, 65, 76:79, 90, 101:104, 115, 126:129, 140)]
  }
  ticker1 <- dat_processed[[1]]
  ticker2 <- dat_processed[[2]]
  ticker3 <- dat_processed[[3]]
  ticker4 <- dat_processed[[4]]
  ticker1$ticker <- 1
  ticker2$ticker <- 2
  ticker3$ticker <- 3
  ticker4$ticker <- 4
  
  x_test <- data.frame(matrix(ncol = 124, nrow = 0))
  names(x_all) <- names(ticker1)
  test_data <- list()
  # Rescale
  for (j in 1:4) {
    x_test <- all_data[[j]]
    for(i in 4:13) x_test[,i] <- scale(x_test[,i], center = e$me_Price.open.Buy, scale = e$sd_Price.open.Buy)
    for(i in 14:23) x_test[,i] <- scale(x_test[,i], center = e$me_Price.open.Sell, scale = e$sd_Price.open.Sell)
    for(i in 24:33) x_test[,i] <- scale(x_test[,i], center = e$me_Price.me.Buy, scale = e$sd_Price.me.Buy)
    for(i in 34:43) x_test[,i] <- scale(x_test[,i], center = e$me_Price.me.Sell, scale = e$sd_Price.me.Sell)
    for(i in 44:53) x_test[,i] <- scale(x_test[,i], center = e$me_Volume.Buy, scale = e$sd_Volume.Buy)
    for(i in 54:63) x_test[,i] <- scale(x_test[,i], center = e$me_Volume.Sell, scale = e$sd_Volume.Sell)
    for(i in 64:73) x_test[,i] <- scale(x_test[,i], center = e$me_Price.weighted.Buy, scale = e$sd_Price.weighted.Buy)
    for(i in 74:83) x_test[,i] <- scale(x_test[,i], center = e$me_Price.weighted.Sell, scale = e$sd_Price.weighted.Sell)
    for(i in 84:93) x_test[,i] <- scale(x_test[,i], center = e$me_Price.close.Buy, scale = e$sd_Price.close.Buy)
    for(i in 94:103) x_test[,i] <- scale(x_test[,i], center = e$me_Price.close.Sell, scale = e$sd_Price.close.Sell)
    for(i in 104:113) x_test[,i] <- scale(x_test[,i], center = e$me_Order.Buy, scale = e$sd_Order.Buy)
    for(i in 114:123) x_test[,i] <- scale(x_test[,i], center = e$me_Order.Sell, scale = e$sd_Order.Sell)
    x_test <- x_test[,(1:124)]
    test_data[[i]] <- x_test
  }
  # Predict
  candidate <- e$candidate
  pred_list <- list()
  for(i in 1:4){
    test_x <- test_data[[i]]
    pred_list[[i]] <- candidate %>% predict(test_x)
  }
  pred1 <- pred_list[[1]]
  pred2 <- pred_list[[2]]
  pred3 <- pred_list[[3]]
  pred4 <- pred_list[[4]]
  return(list(pred1=pred1, pred2=pred2, pred3=pred3, pred4=pred4))
}
