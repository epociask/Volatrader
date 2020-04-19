from distutils.core import setup, Extension 
  
setup(name='sma', 
    ext_modules=[ 
            Extension('fastprime', 
                    ['sma.c'],
                    extra_objects=["c_prime.o"] # Relocatable compiled code of the c_prime to prevent recompiling each time
                    ) 
            ] 
)