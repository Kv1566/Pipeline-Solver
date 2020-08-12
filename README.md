# Pipeline-Solver
# 程式碼完全公開，可隨意使用，也可隨意參與

這是手機遊戲名為Pipeline Adventures的python解題程式，
目前只做好了初始的題目設定界面而已，
正式的解題程式碼還沒開始！ => 解題程式從 1.0.0 版起正式上線！

初學python不久，對於程式碼的精簡及較具效率的寫法並不熟悉，
所以想請路過的python程式高手們有空稍做指導一下，
看看程式碼中有哪些部份是可以再做改善強化的！

另外，也有想要將cells改寫成class，但不知怎麼改寫！ => 終於！從0.6.0版起，cells改寫成class化了！

感謝！

# 版本(各版本都是可獨立運作的)：
* ## Pipeline.2.2.0 - 2020/08/12 (目前最新版本)： <br>
  至此，手動功能已與程式自動解題運算功能同步了！<br>
  目前程式依然停留在只能解到Stage B Level 10的階段，但大部份設想功能大致都已呈現！<br>
  手動部份其實還有幾個功能想做的：<br>
  1. 出題存檔與取檔程式！這樣，才不需要每次要測試時都得重新點畫面出題！<br>
  　不過，這部份太早做其實也會有問題，因為後面有可能再增加新的特殊格子欄位，以致於早期存檔的題目後來有可能會無法正常運作！<br>
    當然，這也可以在未來的程式中加以判斷解決，但總覺得不要太早做比較好，就先暫時放著了！<br>
  2. 出題完後應該有個固定題目的按鈕以便記錄下當時的題目狀況，而另外則有完全回復的按鈕來讓題目回復到最後固定的題目內容去！<br>
  3. 也應該有回復單步與前進單步的設置，這樣才能更加方便的使用手動功能！<br>
  　但，這部份也可能會有問題，就是遇上移動後不可再移動的那種題型時，前進後退一步的動作中需要控制的內容會較複雜些，得小心應對才行！<p>
  
  所以，這些還想做的手動功能，就看情況再來決定是否提前製作了！
  
* ## Pipeline.2.1.0 - 2020/08/12： <br>
  火速改版！因為只是比2.0.0增加了個＂移動時會旋轉＂的格子處理而已，所以花不了多少時間！<br>
  目前程式已經來到了可以解 Stage B Level 10(含) 之前的所有題目了！<br>
  特殊格子已能處理兩種，一種是從Stage A Level 13起的＂移動後不可再被移動＂的綠色格子，在程式裡頭稱之為 moveNoMove！<br>
  另一種則是從Stage B Level 4起的＂移動時會旋轉但仍可繼續被移動＂的藍色格子，在程式裡頭稱之為 rotate！<br>
  而目前還不能處理的是第三種特殊格子：＂全體走兩步後才能開始被移動＂的黃色格子，程式裡將稱之為 move2_canMove，<br>
  這部份會在下一次或下下次改版裡寫完！<br>
  之所以有可能是下下次才寫完，是因為還有個問題要處理，就是上面兩種特殊格子目前都只是自動解題時有處理而已，但人工移動的按鈕尚未處理，<br>
  所以，下次改版有可能會先將人工按鈕同步處理完後再來寫第三種特殊格子的解法！
  
* ## Pipeline.2.0.0 - 2020/08/12： <br>
  這個版本原本命名為1.1.0的版本編號，但因實際與1.0.0版有不小的差異！故，想想後還是改編為2.0.0版好了！<br>
  由於從Stage A Level 13起加入了新的＂移動後便不可再被移動＂的格子，因此為因應這個特殊格子，程式碼部份結構必須配合做改變！<br>
  有心研究其間差異者，請自行觀察1.0.0版與2.0.0版之間所有有差異的程式碼，慢慢去理解它們！<br>
  目前所修改的程式碼還不成熟，它只是確定能解Stage A Level 13～16而已，<br>
  至於下一個Stage(B)還能不能適用？是否有細節還得再做更精密調整或甚至大變動，就不得而知了！＝＞已確認能解至Stage B Level 3<br>
  
* ## Pipeline.1.0.0 - 2020/08/11： <br>
  程式解題正式上路！<br>
  目前能解的題目為Stage A Level 1～12！Stage A Level 13起則尚不能解!<br>
  Stage A Level 13起之關卡因為有加入移動後變為不可再動之格子，此部份尚未在程式中處理，故尚不能解！<br>
  Stage A Level 1～12之題目，找時間再貼上來！若有下載此遊戲者可自行先玩玩看！
  
* ## Pipeline.0.6.0 - 2020/08/11： <br>
  自此版開始，cells開始物件化，改寫成以class型式呈現！<br>
  這樣，每個cell中的up, right, down, left, ...等等項目，就不必再在三維陣列裡摸索位置了，<br>
  每個項目都可以很直觀的使用它們各自的屬性處理！
  
* ## Pipeline.0.5.0 - 2020/08/10： <br>
  ps. 0.5.0曾有錯誤，已修正！若在2020/08/10-19:37:00前下載者，請重新下載！<br>
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
