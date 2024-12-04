# Python projects

## OpenCV 
### CatsBlur.py
<p>Это программа предназначена для поиска на изображении объекта, для этого я использовал фильтр Canny и Гаусово размытие. Для того чтобы убрать промежуточные помехи я использовал морфологию</p>

![Canny](./readmeImg/img.png)
```python
canny = cv2.Canny(img,0,255)
```
![GaussianBlur](./readmeImg/img_3.png)

```python
blur = cv2.GaussianBlur(img,(59,59),1)
```

### Les13112024FindContours.py

<p>Эта программа находит объекты на изображении, можно регулировать цветовым пространством с помощью ползунков. Можно регулировать пороговые значения площади</p>

![GaussianBlur](./readmeImg/img_4.png)

```python

thresh = cv2.inRange( hsv, hsv_max, hsv_min )

contour,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

```
<p> первая команда создает маску для изображения, особо интересные цвета обозначаем белым, остальное черным. Вторая команда находит контура</p>

![GaussianBlur](./readmeImg/img_5.png)

### ApproxFindFigure.py

<p>Эта программа позволяет находить различные формы на изображении</p>

![ApproxFindFigure](./readmeImg/img_6.png)


### GaussianBlur.py

<p>Эта программа позволяет работать с изображениями, применять фильтр Canny, исспользовать морфологию</p>

![GaussianBlur](./imgGit/img.png)


### CannyAndBlur.py

<p>Эта программа позволяет работать с изображениями, применять фильтр Canny, исспользовать морфологию</p>

![Canny](./imgGit/img_1.png)


### HaarCascade

<p>Обнаружение лиц с помощью HaarCascade</p>

![HaarCascade](./imgGit/cascade.png)


### Distance to camera 

<p>Обнаружение расстояния до камеры. Если мы находимся слишком близко к камере, то загарается красный квадрат и появляется надпись с предупреждением</p>

![Cascade](./imgGit/img_2.png)
![Cascade](./imgGit/img_3.png)