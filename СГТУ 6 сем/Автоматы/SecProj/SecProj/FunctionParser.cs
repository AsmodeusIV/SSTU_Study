using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SecProj
{
    using System;
    using System.Collections.Generic;
    using System.Text;

    public class FunctionParser
    {
        private struct SynTable
        {
            public string ChSet; // Множество символов
            public int Go;      // Переход
            public bool Err;    // Ошибка
            public bool Call;   // Вызов
            public bool Read;   // Читать
            public int Proc;    // Процедура
        }

        private SynTable[] T;   // Таблица
        private char Ch;        // Текущий символ
        private int Err;        // Признак ошибки
        private Stack<int> Stack; // Стек
        private int i;          // Номер состояния
        private string input;   // Входная строка
        private int pos;        // Позиция в строке

        // Семантические переменные
        private int A, B;
        private List<string> variables = new List<string>();
        private Dictionary<string, double> varValues = new Dictionary<string, double>();
        private StringBuilder currentVar = new StringBuilder();

        public FunctionParser()
        {
            InitializeTable();
        }

        private void InitializeTable()
        {
            T = new SynTable[21];

            // Состояние 1: Начало числа A
            T[1] = new SynTable { ChSet = "0123456789", Go = 2, Err = false, Call = false, Read = true, Proc = 1 };

            // Состояние 2: Продолжение числа A
            T[2] = new SynTable { ChSet = "0123456789", Go = 2, Err = false, Call = false, Read = true, Proc = 1 };

            // Состояние 3: Пропуск пробелов после A
            T[3] = new SynTable { ChSet = " ", Go = 3, Err = false, Call = false, Read = true, Proc = 0 };
            T[4] = new SynTable { ChSet = "*", Go = 5, Err = true, Call = false, Read = true, Proc = 0 };

            // Состояние 5: Пропуск пробелов после первого *
            T[5] = new SynTable { ChSet = " ", Go = 5, Err = false, Call = false, Read = true, Proc = 0 };

            // Состояние 6: Начало числа B
            T[6] = new SynTable { ChSet = "0123456789", Go = 7, Err = true, Call = false, Read = true, Proc = 2 };

            // Состояние 7: Продолжение числа B
            T[7] = new SynTable { ChSet = "0123456789", Go = 7, Err = false, Call = false, Read = true, Proc = 2 };

            // Состояние 8: Пропуск пробелов после B
            T[8] = new SynTable { ChSet = " ", Go = 8, Err = false, Call = false, Read = true, Proc = 0 };
            T[9] = new SynTable { ChSet = "*", Go = 10, Err = true, Call = false, Read = true, Proc = 0 };

            // Состояние 10: Пропуск пробелов после второго *
            T[10] = new SynTable { ChSet = " ", Go = 10, Err = false, Call = false, Read = true, Proc = 0 };
            T[11] = new SynTable { ChSet = "(", Go = 12, Err = true, Call = false, Read = true, Proc = 0 };

            // Состояние 12: Пропуск пробелов после '('
            T[12] = new SynTable { ChSet = " ", Go = 12, Err = false, Call = false, Read = true, Proc = 0 };

            // Состояние 13: Начало переменной
            T[13] = new SynTable
            {
                ChSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                Go = 14,
                Err = true,
                Call = false,
                Read = true,
                Proc = 3
            };

            // Состояние 14: Продолжение переменной
            T[14] = new SynTable
            {
                ChSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                Go = 14,
                Err = false,
                Call = false,
                Read = true,
                Proc = 3
            };

            // Состояние 15: Пропуск пробелов после переменной
            T[15] = new SynTable { ChSet = " ", Go = 15, Err = false, Call = false, Read = true, Proc = 0 };
            T[16] = new SynTable { ChSet = "+", Go = 17, Err = false, Call = false, Read = true, Proc = 0 };

            // Состояние 17: Пропуск пробелов после '+'
            T[17] = new SynTable { ChSet = " ", Go = 17, Err = false, Call = false, Read = true, Proc = 0 };

            // Состояние 18: Ожидается следующая переменная или ')'
            T[18] = new SynTable
            {
                ChSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                Go = 13,
                Err = false,
                Call = false,
                Read = false,
                Proc = 0
            };
            T[19] = new SynTable { ChSet = ")", Go = 20, Err = false, Call = false, Read = true, Proc = 4 };

            // Состояние 20: Конец функции
            T[20] = new SynTable { ChSet = "\0", Go = 0, Err = false, Call = false, Read = false, Proc = 5 };
        }

        private void NextCh()
        {
            if (pos < input.Length)
            {
                Ch = input[pos++];
            }
            else
            {
                Ch = '\0';
            }
        }

        private bool IsInSet(char c, string set)
        {
            if (set == "любой") return true;
            if (set == "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                return char.IsLetter(c);
            if (set == "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                return char.IsLetterOrDigit(c);
            return set.Contains(c.ToString());
        }

               public bool Parse(string expression)
        {
            input = expression + '\0';
            pos = 0;
            Err = 0;
            A = 0;
            B = 0;
            variables.Clear();
            varValues.Clear();
            currentVar.Clear();
            Stack = new Stack<int>();
            Stack.Push(0);
            i = 1;

            NextCh();

            do
            {
                if (IsInSet(Ch, T[i].ChSet) || T[i].ChSet == "любой")
                {

                    if (T[i].Read) NextCh();

                    if (T[i].Go == 0)
                    {
                        if (Stack.Count > 0)
                        {
                            i = Stack.Pop();
                        }
                        else
                        {
                            break;
                        }
                    }
                    else
                    {
                        if (T[i].Call) Stack.Push(i + 1);
                        i = T[i].Go;
                    }
                }
                else
                {
                    if (T[i].Err)
                    {
                        Err = i;
                        break;
                    }
                    else
                    {
                        i++;
                    }
                }
            } while (i != 0 && Err == 0);

            if (Err != 0)
            {
                throw new Exception($"Ошибка синтаксиса в состоянии {i} (символ: '{Ch}')");
                Console.WriteLine($"Ожидались символы из множества: {T[i].ChSet}");
                return false;
            }

            return true;
        }
    }


}
