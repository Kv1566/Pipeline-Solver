# Pipeline-Solver
# 程式碼完全公開，可隨意使用，也可隨意參與

這是手機遊戲名為Pipeline Adventures的python解題程式，
目前只做好了初始的題目設定界面而已，
正式的解題程式碼還沒開始！

初學python不久，對於程式碼的精簡及較具效率的寫法並不熟悉，
所以想請路過的python程式高手們有空稍做指導一下，
看看程式碼中有哪些部份是可以再做改善強化的！

另外，也有想要將cells改寫成class，但不知怎麼改寫！

感謝！

# 版本(各版本都是可獨立運作的)：
* ## Pipeline.0.5.0 - 2020/08/10 (目前最新版本)： <br>
  這一版與0.4.0的內容絕大部份是完全一模一樣的，差別在i與j, x與y的順序對調！<br>
  其實，眼尖的高手應該有發現，原本0.4.0中的陣列內容是行列反置的，主要是因為一開始建立二維陣列時就搞錯了！<br>
  因為當時沒注意，又急著繼續寫程式，結果就將錯就錯一直寫下去！<br>
  但，接下去要寫解題程式，這樣行列反置的情況真的會把大腦給搞壞，<br>
  所以，就趁著程式內容還不算太大，而現在腦袋剛好還夠清楚，就趕緊把所有i,j,x,y相反的內容全導正回來！<br>
  i,j兩者皆存在時，i會代表row，j會代表col，<br>
  x1,y1 或 x2,y2 同時存在時，x會代表row，y會代表col<br>
  這樣，思考路徑應該就不會混亂了！
  
* ## Pipeline.0.4.0 - 2020/08/10： <br>
  上下左右以人工按鈕方式移動格子的功能已經完成！<br>
  此部份程式碼有點亂, 比較偏向土法煉鋼方式寫成，<br>
  暫時還不知道如何整理並精簡此部份的程式碼，但它卻是可以正常運作的！<br>
  精簡工作只好等日後再說！<br>
  或者，路過的高手們可以幫忙指點一下！感謝！<br>
  至此，人工運作方面的程式碼大致已完成，接下去便是要開始做程式解題的部份了！<br>
  畫面右上角多出了兩個按鈕，讀取與存檔！那是將來要用來儲存題目及提供讀題用的，以後回頭再寫！
  
* ## Pipeline.0.3.1 - 2020/08/09： <br>
  這版只是將0.3.0的內容中的四組按鈕(上下左右)賦予按鈕功能而已<br>
  按鈕的結果目前尚未真正寫作，目前是先處理所有按鈕的辨識<br>
  辨識很重要，之後才能根據辨識來判定哪個按鈕被按下而做出相對應的動作<br>
  目前做的這些按鈕，將來主要是用來做為人工移動格子用的！
  
* ## Pipeline.0.3.0 - 2020/08/09： <br>
  其實這版本內容是與0.2.0一樣的，只是將之改成Class APP模式而已<br>
  我也不知道寫成Class模式好，還是維持原本0.2.0的型式好<br>
  Class模式看起來比較高級，原本0.2.0模式比較簡單<br>
  解題部份一樣尚未寫作<br>
  預計下週有空開始寫吧！
  
* ## Pipeline.0.2.0 - 2020/08/06： <br>
  rows及cols可在視窗中任意更改以變更格子m*n大小<br>
  上下右右移動按鈕，暫時備用而已<br>
  解題尚未寫作
  
* ## Pipeline.py - 2020/08/03： <br>
  初始版本

MarkDown語法參考頁:https://github.com/emn178/markdown
