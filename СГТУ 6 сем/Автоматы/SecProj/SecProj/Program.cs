namespace SecProj
{
    internal class Program
    {
        static void Main(string[] args)
        {
            List<string> list = new List<string>() { "12*34*(x+y+z)", "5 * 5 * ( l1 + l2 + l3 )", "5*(-5)*(l1+l2+l3)", "5*(-5)*(l1+l2-l3)", "5*-5)*(3+l1)", "5*(-5)*(3+l1)", ";5*(-5)*(3+l1)" };
            var parser = new RecursiveParser();
            FunctionParser parser1 = new FunctionParser();
            foreach (string input in list)
            {
                try
                {
                    Console.WriteLine("Выражение вида A*B*(x1+x2+...+xn): " + input);
                    parser1.Parse(input);
                    //parser.StartParse(input);
                    Console.WriteLine("Синтаксический анализ завершен успешно.");

                    //double result = parser.Evaluate();
                    //Console.WriteLine($"Результат вычисления: {result}");
                    Console.WriteLine("\n");
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}
