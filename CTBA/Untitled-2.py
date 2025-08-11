import matplotlib.pyplot as plt

print("plt.style.available:")
styles = plt.style.available

for style in styles:
        print("style:", style)


plt.plot([1, 2, 3, 4], [1, 8, 27, 64])
plt.axis([0, 5, 0, 70]) 
plt.xlabel("Integers (1-4)") 
plt.ylabel("Cubed Integers") 
plt.show()