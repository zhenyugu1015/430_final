myPred_myGroupNumber <- function("path\to\Ticker1.csv", "path\to\Ticker2.csv",
                                 "path\to\Ticker3.csv", "path\to\Ticker4.csv",
                                 "path\to\myCandidateModel")
{
  # the function should automatically handle the 4 raw file inputs and prepare
  # whatever features that are to be fed into your trained candidate model
  ...
  # 1. `pred1` is a vector of predicted labels associated with each available
  # trading second in "Ticker1.csv"
  # 2. the order of `pred1` should be chronologically from the first available
  # second to the last available second of "Ticker1.csv"
  # 3. similarly for `pred2`, `pred3`, and `pred4`
  return(list(pred1=pred1, pred2=pred2, pred3=pred3, pred4=pred4))
}
