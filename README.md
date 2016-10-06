# heart-of-gold
Modelling Atrial Fibrillation using Cellular Automata

Dysfunctional cells or probabilty based propagation not implemented yet.

Example of using the code:

```python
a = base.heart(100,100)
a.excite(49,49)       #excites cell at coodinates given
a.create_anifigure()      #needs to be done before the simulation
a.iterate(100,False)      #False dictates that no new pulses will propagate (set to True if you want a beating heart) 
												  #	--> a.iterate(100,True,50)
a.show_animation()        #shows a preview of the animation (can't use again after first viewing?)
a.save_animation("test")
```
