# Power Trading
NCKU DSAI HW3 - Power Trading

Design an agent for bidding power to minimize your electricity bill.

## Trader Strategy
計算預測的產電量與用電量之間的差值，當產電量大於用電量即表示持有多餘電量，為求不出現浪費的電，以最低價將多餘的電量進行投標販賣，反之若產電量小於用電量則表示電量無法自給自足，需要購買電以補足用電所需，因此以洽低於市電單價的價格進行所缺用電量的投標購買，結束前述判斷之後再將當前所持有的剩餘電量全數以略高於市電單價的價格進行販賣，以求能賺取更多利益。由於模型預測結果必須要精準預測缺電量、多餘電量，為了不受到預測不準的影響，我們改選擇使用保守的規則來進行電量的交易。

```
多餘電量 = 產電量 - 用電量
```
|           | target value | target price | action |
|:---------:|:------------:|:------------:|:------:|
|多餘電量 > 0| 多餘電量 </br> 產電量 - 多餘電量 | 0.01 </br> 2.53 | sell </br> sell |
|多餘電量 < 0| -多餘電量 </br> 產電量 | 2.52 </br> 2.53 | buy </br> sell |

## Code Execution
Environment: ```Python 3.8.13```

- Install packages
```
$ pipenv install requests
```
- Execute ```main.py```
```
$ pipenv run python main.py
```