# Autoeins [AUTO 1]

The problem is about routing one truck between branchs containing each one a number of vehicles to deliver to a logistic park which is the start point of the truck.
</br>
We consider here the first 6 "arrondissements" of Paris.
</br>
</br>
<img src="https://blog.locservice.fr/wp-content/uploads/2017/08/location-appartement-paris-1024x854.jpg" width="350" height="350" style="display: block;margin-left: auto;margin-right: auto;width: 50%"/>
</br>
</br>
</br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\forall&space;i,j&space;\epsilon&space;\left&space;\{&space;1&space;\right&space;,...,n\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\forall&space;i,j&space;\epsilon&space;\left&space;\{&space;1&space;\right&space;,...,n\}" title="\forall i,j \epsilon \left \{ 1 \right ,...,n\}" /></a></br></br>
<a href="https://www.codecogs.com/eqnedit.php?latex=objectif1&space;=max\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}v_{ij}x_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?objectif1&space;=max\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}v_{ij}x_{ij}" title="objectif1 =max\sum_{i =1}^{n}\sum_{j =1}^{n}v_{ij}x_{ij}" /></a></br></br>
<a href="https://www.codecogs.com/eqnedit.php?latex=objectif2&space;=min\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}c_{ij}x_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?objectif2&space;=min\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}c_{ij}x_{ij}" title="objectif2 =min\sum_{i =1}^{n}\sum_{j =1}^{n}c_{ij}x_{ij}" /></a></br></br>
<a href="https://www.codecogs.com/eqnedit.php?latex=finalObjective&space;=\omega_{0}objectif1&plus;\omega_{1}objectif2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?finalObjective&space;=\omega_{0}objectif1&plus;\omega_{1}objectif2" title="finalObjective =\omega_{0}objectif1+\omega_{1}objectif2" /></a></br></br>
<a href="https://www.codecogs.com/eqnedit.php?latex=finalObjectif&space;=max\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}a_{ij}x_{ij};&space;\:&space;\:&space;a_{ij}&space;=&space;\omega_{0}v_{ij}&space;-&space;\omega_{1}c_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?finalObjectif&space;=max\sum_{i&space;=1}^{n}\sum_{j&space;=1}^{n}a_{ij}x_{ij};&space;\:&space;\:&space;a_{ij}&space;=&space;\omega_{0}v_{ij}&space;-&space;\omega_{1}c_{ij}" title="finalObjectif =max\sum_{i =1}^{n}\sum_{j =1}^{n}a_{ij}x_{ij}; \: \: a_{ij} = \omega_{0}v_{ij} - \omega_{1}c_{ij}" /></a></br></br>

<a href="https://www.codecogs.com/eqnedit.php?latex=v_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?v_{ij}" title="v_{ij}" /></a>
: Sum of vehicles between branch i and j

<a href="https://www.codecogs.com/eqnedit.php?latex=c_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c_{ij}" title="c_{ij}" /></a>
: Cost (distance) between branch i and j
</br>
</br>
</br>
</br>
<a href="https://www.codecogs.com/eqnedit.php?latex=x_{ij}&space;=&space;\left\{\begin{matrix}&space;1&space;\:&space;\:&space;\:&space;\:&space;\:&space;if&space;\:&space;\:&space;\:&space;j&space;\:&space;\:&space;selected&space;\:&space;\:&space;from&space;\:&space;\:&space;\:&space;i&space;&&space;\\&space;0&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;otherwise&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?x_{ij}&space;=&space;\left\{\begin{matrix}&space;1&space;\:&space;\:&space;\:&space;\:&space;\:&space;if&space;\:&space;\:&space;\:&space;j&space;\:&space;\:&space;selected&space;\:&space;\:&space;from&space;\:&space;\:&space;\:&space;i&space;&&space;\\&space;0&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;\:&space;otherwise&space;&&space;\end{matrix}\right." title="x_{ij} = \left\{\begin{matrix} 1 \: \: \: \: \: if \: \: \: j \: \: selected \: \: from \: \: \: i & \\ 0 \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: \: otherwise & \end{matrix}\right." /></a>
</br>
</br>
</br>
</br>

<a href="https://www.codecogs.com/eqnedit.php?latex=T&space;\leqslant&space;8;\:&space;\:&space;T:&space;the\:&space;\:&space;truck&space;\:&space;\:&space;loaded&space;\:&space;\:vehicles" target="_blank"><img src="https://latex.codecogs.com/gif.latex?T&space;\leqslant&space;8;\:&space;\:&space;T:&space;the\:&space;\:&space;truck&space;\:&space;\:&space;loaded&space;\:&space;\:vehicles" title="T \leqslant 8;\: \: T: the\: \: truck \: \: loaded \: \:vehicles" /></a>
</br>
</br>
</br>
<a href="https://www.codecogs.com/eqnedit.php?latex=7\leq&space;time&space;\leqslant&space;17;\:&space;\:&space;time:&space;the\:&space;\:work\:&space;\:&space;time&space;\:&space;\:&space;window\:&space;\:of\:&space;\:&space;the\:&space;\:&space;logistic\:&space;\:&space;park" target="_blank"><img src="https://latex.codecogs.com/gif.latex?7\leq&space;time&space;\leqslant&space;17;\:&space;\:&space;time:&space;the\:&space;\:work\:&space;\:&space;time&space;\:&space;\:&space;window\:&space;\:of\:&space;\:&space;the\:&space;\:&space;logistic\:&space;\:&space;park" title="7\leq time \leqslant 17;\: \: time: the\: \:work\: \: time \: \: window\: \:of\: \: the\: \: logistic\: \: park" /></a>
</br>
</br>
</br>

<a href="https://www.codecogs.com/eqnedit.php?latex=P_{00}&space;\leq&space;3&space;;\:&space;\:&space;P_{00}:&space;the\:&space;\:\:\:\:\:\:\:\:\:number\:\:\:\:\:\:\&space;of&space;\\&space;\:&space;\:&space;branchs\:&space;\:served\:&space;\:&space;before&space;\:&space;\:&space;returning\:&space;\:&space;to\:&space;\:&space;logistic\:&space;\:&space;park" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P_{00}&space;\leq&space;3&space;;\:&space;\:&space;P_{00}:&space;the\:&space;\:\:\:\:\:\:\:\:\:number\:\:\:\:\:\:\&space;of&space;\\&space;\:&space;\:&space;branchs\:&space;\:served\:&space;\:&space;before&space;\:&space;\:&space;returning\:&space;\:&space;to\:&space;\:&space;logistic\:&space;\:&space;park" title="P_{00} \leq 3 ;\: \: P_{00}: the\: \:\:\:\:\:\:\:\:\:number\:\:\:\:\:\:\ of \\ \: \: branchs\: \:served\: \: before \: \: returning\: \: to\: \: logistic\: \: park" /></a>
