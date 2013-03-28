from forms.curve import koch

reload( koch )


koch1 = koch.Koch()
koch1.curve()
x = koch1.drawCurve()

koch2 = koch.Koch()
koch2.snowflake()
y = koch2.drawCurve()

print x
print y

# Result: curve1
# Result: curve2

