from cacaodocs import CacaoDocs

class Calculator:
    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def add(self, a, b):
        """
        Method: add
        Version: v1
        Status: Production
        
        Description:
            Adds two numbers together.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The sum of a and b
        """
        return a + b

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def subtract(self, a, b):
        """
        Method: subtract
        Version: v1
        Status: Production
        
        Description:
            Subtracts second number from first number.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The difference between a and b
        """
        return a - b

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def multiply(self, a: float, b: float) -> float:
        """
        Method: multiply
        Version: v1
        Status: Production
        
        Description:
            multiply two numbers together.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The difference between a and b
        """
        return a * b

    def divide(self, a, b):
        if b != 0:
            return a / b
        else:
            raise ValueError("Cannot divide by zero")

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def calculator_status_check(self) -> str:
        """
        Method: calculator_status_check
        Version: v1
        Status: Production

        Description:
            Check if the calculator is operational.

        Returns:
            @type{str}: The operational status of the calculator
        """
        return "Calculator is operational", 200