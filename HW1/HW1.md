## 计算摄像学第一次作业

**光度立体视觉**

1600012785 朱文韬



三道题的源码以对应编号命名。

1. 结果见`results/5_objects`

   采用了经典方法，朗伯反射+方向标定的平行光源，利用最小二乘求解优化问题，参考了课件的代码。

2. 结果见`results/DiLiGenT`

```
Case bearPNG, Err=21.10689
Case cowPNG, Err=27.57731
Case catPNG, Err=17.61255
Case readingPNG, Err=25.85098
Case pot1PNG, Err=18.41141
Case ballPNG, Err=16.55320
Case pot2PNG, Err=21.58637
Case harvestPNG, Err=34.73090
Case gobletPNG, Err=23.22053
Case buddhaPNG, Err=20.76103
```

分析：总体来说，在形状较规则、平滑的物体上表现好（如ball,cat,pot1）。在褶皱的物体上表现不好（如Harvest），这主要与朗伯反射的假设有关。

3. 结果见`results/DiLiGenT_threshold`

```
Case bearPNG, Err=21.06868
Case cowPNG, Err=21.98639
Case catPNG, Err=18.48923
Case readingPNG, Err=24.78296
Case pot1PNG, Err=20.50712
Case ballPNG, Err=19.02789
Case pot2PNG, Err=21.25987
Case harvestPNG, Err=31.87154
Case gobletPNG, Err=21.86597
Case buddhaPNG, Err=22.03358
```

分析：合适的thresholding能够减小error，原因是treshold去掉了一些阴影、过曝等不希望引入的信息，减小了噪声。也有几个case里error略有提高，可能是因为treshold之后可用的信息减少了。

