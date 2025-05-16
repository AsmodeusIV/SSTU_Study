using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SecProj
{
    internal class RecursiveParser
    {
        private string input;
        private int position;
        private char currentChar;
        private Dictionary<string, double> variables = new Dictionary<string, double>();

        private int A, B;
        private List<string> variableNames = new List<string>();

        public void StartParse(string input)
        {
            this.input = input;
            this.position = 0;
            this.currentChar = input.Length > 0 ? input[0] : '\0';
            variableNames = new List<string>();
            variables = new Dictionary<string, double>();

            SkipWhitespace();
            ParseExpression();

            if (currentChar != '\0')
            {
                Error("Ожидается конец выражения");
            }
        }

        private void Error(string message)
        {
            string errorPointer = new string(' ', position) + "^";
            throw new Exception($"Ошибка в позиции {position}: {message}\n{input}\n{errorPointer}");
        }

        private void Advance()
        {
            position++;
            currentChar = position < input.Length ? input[position] : '\0';
        }

        private void SkipWhitespace()
        {
            while (currentChar == ' ')
            {
                Advance();
            }
        }

        private void Match(char expected)
        {
            if (currentChar == expected)
            {
                Advance();
                SkipWhitespace();
            }
            else
            {
                Error($"Ожидается '{expected}', но получено '{currentChar}'");
            }
        }

        private void ParseExpression()
        {
            A = ParseInteger();
            Match('*');
            B = ParseInteger();
            Match('*');
            Match('(');
            ParseVariableList();
            Match(')');
        }

        private int ParseInteger()
        {
            string numStr = "";
            bool isNegative = false;
            bool hasParentheses = false;

            if (currentChar == '(')
            {
                hasParentheses = true;
                Match('(');
            }

            if (currentChar == '-')
            {
                isNegative = true;
                numStr += currentChar;
                Advance();
            }
            else if (currentChar == '+')
            {
                Advance();
            }

            if (!char.IsDigit(currentChar))
            {
                Error("Ожидается целое число");
            }

            while (char.IsDigit(currentChar))
            {
                numStr += currentChar;
                Advance();
            }

            if (hasParentheses)
            {
                Match(')');
            }

            SkipWhitespace();

            int result = int.Parse(numStr);
            return result;
        }

        private void ParseVariableList()
        {
            ParseVariable();

            while (currentChar == '+')
            {
                Match('+');
                ParseVariable();
            }
        }

        private void ParseVariable()
        {
            string varName = "";

            if (!char.IsLetter(currentChar))
            {
                Error("Ожидается имя переменной (начинается с буквы)");
            }

            while (char.IsLetterOrDigit(currentChar))
            {
                varName += currentChar;
                Advance();
            }

            SkipWhitespace();
            variableNames.Add(varName);
        }

        public double Evaluate()
        {
            foreach (var varName in variableNames)
            {
                if (!variables.ContainsKey(varName))
                {
                    System.Console.Write($"Введите значение переменной {varName}: ");
                    double value;
                    while (!double.TryParse(System.Console.ReadLine(), out value))
                    {
                        System.Console.Write("Некорректный ввод. Введите вещественное число: ");
                    }
                    variables[varName] = value;
                }
            }

            double sum = 0;
            foreach (var varName in variableNames)
            {
                sum += variables[varName];
            }

            return A * B * sum;
        }
    }
}
