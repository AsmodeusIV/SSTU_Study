using System.Text;

/*
 n работ могут исполняться n исполнителями. Известно время исполнения каждой работы каждым исполнителем: t_{ij}\ i=1..n,\ j=1..n. Распределить работы между исполнителями так, чтобы каждая работа выполнялась одним исполнителем, каждый исполнитель выполнял одну работу, а суммарное время выполнения всех работ было минимальным
*/

class AssignmentProblem
{
    enum AlgorithmType
    {
        ALG_HEURISTIC,
        ALG_BRUTEFORCE
    }

    private int option;

    private int n;
    private int[,] T;
    private AlgorithmType algorithmType;

    public AssignmentProblem()
    {
    }

    private void showData(int[,] C)
    {
        StringBuilder sb = new StringBuilder("\n=======================\n");
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                sb.Append(C[i, j] + " ");
            }
            sb.AppendLine(); // Переход на новую строку после каждой строки массива
        }
        sb.AppendLine("=======================");
        Console.Write(sb.ToString());
    }

    private void saveData(int[,] C)
    {
        Console.Write("Сохранение исходных данных - введите имя файла: ");
        string filePath = Console.ReadLine();
        WriteDataToFile(C, filePath);
    }

    public void WriteDataToFile(int[,] T, string filePath)
    {
        int n = T.GetLength(0);
        StringBuilder sb = new StringBuilder();

        sb.AppendLine(n.ToString());

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                sb.Append(T[i, j] + " ");
            }
            sb.AppendLine(); // Переход на новую строку после каждой строки массива
        }

        // Запись данных в файл
        File.WriteAllText(filePath, sb.ToString());
    }

    public int[,] ReadDataFromFile(string filePath)
    {
        string[] fileLines = File.ReadAllLines(filePath);
        n = Convert.ToInt32(fileLines[0]);
        T = new int[n, n];
        for (int i = 0; i < n; i++)
        {
            int[] times = fileLines[i + 2].Split(' ').Select(int.Parse).ToArray();
            for (int j = 0; j < n; j++)
            {
                T[i, j] = times[j];
            }
        }
        return T;
    }

    private void BruteForceAssignment(int[,] T)
    {
        int n = T.GetLength(0);
        int[] workers = Enumerable.Range(0, n).ToArray();
        int minTotalTime = int.MaxValue;
        int[] bestAssignment = new int[n];

        Permute(workers, 0, n - 1);

        void Permute(int[] arr, int l, int r)
        {
            if (l == r)
            {
                int totalTime = 0;
                for (int i = 0; i < n; i++)
                {
                    totalTime += T[i, arr[i]];
                }

                if (totalTime < minTotalTime)
                {
                    minTotalTime = totalTime;
                    arr.CopyTo(bestAssignment, 0);
                }
            }
            else
            {
                for (int i = l; i <= r; i++)
                {
                    Swap(ref arr[l], ref arr[i]);
                    Permute(arr, l + 1, r);
                    Swap(ref arr[l], ref arr[i]); // backtrack
                }
            }
        }

        void Swap(ref int a, ref int b)
        {
            int temp = a;
            a = b;
            b = temp;
        }

        for (int i = 0; i < n; i++)
        {
            Console.WriteLine($"Работник {i + 1} выполняет работу {bestAssignment[i] + 1}");
        }
        Console.WriteLine($"Минимальное общее время: {minTotalTime}");
    }


    private IEnumerable<List<int>> GetPermutations(List<int> list, int length)
    {
        if (length == 1) return list.Select(t => new List<int> { t });

        return GetPermutations(list, length - 1)
        .SelectMany(t => list.Where(e => !t.Contains(e)),
        (t1, t2) => t1.Concat(new List<int> { t2 }).ToList());
    }


    private void GreedyAssignment(int[,] T)
    {
        int n = T.GetLength(0);
        bool[] assignedJobs = new bool[n];
        bool[] assignedWorkers = new bool[n];
        int minTotalTime = 0; // Инициализация переменной для хранения общего минимального времени

        for (int i = 0; i < n; i++)
        {
            int minTime = int.MaxValue;
            int worker = -1;
            int job = -1;

            for (int j = 0; j < n; j++)
            {
                if (!assignedWorkers[j])
                {
                    for (int k = 0; k < n; k++)
                    {
                        if (!assignedJobs[k] && T[j, k] < minTime)
                        {
                            minTime = T[j, k];
                            worker = j;
                            job = k;
                        }
                    }
                }
            }

            

            if (worker != -1 && job != -1) // Проверка, что работник и работа были найдены
            {
                assignedJobs[job] = true;
                assignedWorkers[worker] = true;
                minTotalTime += minTime; // Добавление времени выполнения работы к общему времени
                Console.WriteLine($"Работник {worker + 1} выполняет работу {job + 1} за {minTime}");
            }
        }
        // Вывод общего минимального времени после назначения всех работ
        Console.WriteLine($"Минимальное общее время: {minTotalTime}");
    }

    public void Dialogue()
    {
        bool loop = true;
        string filePath;
        while (loop)
        {

            Console.WriteLine("Выбор типа алгоритма:");
            Console.WriteLine("1. Эвристический алгоритм (быстрый, но не точный)");
            Console.WriteLine("2. Алгоритм перебора (медленный, точный)");
            option = GetUserOption(1, 2);

            switch (option)
            {
                case 1:
                    algorithmType = AlgorithmType.ALG_HEURISTIC;
                    break;
                case 2:
                    algorithmType = AlgorithmType.ALG_BRUTEFORCE;
                    break;
            }

            Console.WriteLine("Ввод исходных данных:");
            Console.WriteLine("1. С клавиатуры");
            Console.WriteLine("2. Случайные значения");
            Console.WriteLine("3. Восстановить исходные данные");

            option = GetUserOption(1, 3);

            switch (option)
            {
                case 1:
                    n = GetValidIntegerValue("Введите число работников n: ");

                    T = new int[n, n];

                    for (int i = 0; i < n; i++)
                    {
                        for (int j = 0; j < n; j++)
                        {
                            T[i, j] = GetValidIntegerValue($"Введите надежность блока [{j + 1}:{i + 1}] = ");
                        }
                    }
                    saveData(T);
                    showData(T);
                    break;

                case 2:
                    var random = new Random();
                    n = GetValidIntegerValue("Введите число работников n: ");
                    T = new int[n, n];
                    for (int i = 0; i < n; i++)
                    {
                        for (int j = 0; j < n; j++)
                        {
                            T[i, j] = random.Next(1, 24);
                        }
                    }
                    saveData(T);
                    showData(T);
                    break;

                case 3:
                    bool valid;
                    do
                    {
                        valid = true;
                        Console.Write("Введите путь к файлу c исходными данными: ");
                        filePath = Console.ReadLine();
                        string[] fileLines = File.ReadAllLines(filePath);
                        n = Convert.ToInt32(fileLines[0]);
                        T = new int[n, n];
                        for (int i = 0; i < n; i++)
                        {
                            int[] times = fileLines[i + 2].Trim().Split(' ').Select(int.Parse).ToArray();
                            for (int j = 0; j < n; j++)
                            {
                                T[i, j] = times[j];
                            }
                        }

                        if (n <= 0)
                        {
                            Console.WriteLine("Ошибка: n или m должно быть больше нуля. Пожалуйста, введите данные заново.");
                            valid = false;
                        }
                        else
                        {
                            for (int i = 0; i < n; i++)
                            {
                                for (int j = 0; j < n; j++)
                                {
                                    if (T[i, j] <= 0)
                                    {
                                        Console.WriteLine("Надежность блока должна быть больше нуля. Пожалуйста, введите корректные данные.");
                                        valid = false;
                                        break;
                                    }
                                }
                                if (!valid) break;
                            }
                            showData(T);
                        }
                    } while (!valid);
                    break;
            }

            if (algorithmType == AlgorithmType.ALG_HEURISTIC)
            {
                 GreedyAssignment(T);
            }

            else
            {
                BruteForceAssignment(T);
            }

            Console.WriteLine("1 - Возврат в меню");
            Console.WriteLine("0 - Завершение работы");

            option = GetUserOption(0, 1);

            switch (option)
            {
                case 1:
                    continue; // Возврат в начало цикла while
                case 0:
                    loop = false; // Выход из цикла while и завершение программы
                    break;
            }
        }
    }

    public int GetUserOption(int low, int high)
    {
        while (true)
        {
            Console.Write($"Выберите опцию ({low} - {high}): ");
            string input = Console.ReadLine();
            string digitOnly = new string(input.Where(char.IsDigit).ToArray());
            int option;
            if (int.TryParse(digitOnly, out option) && (option >= low && option <= high))
            {
                return option;
            }
            Console.WriteLine($"Ошибка! Пожалуйста, выберите нужную опцию в пределах {low} - {high}");
        }
    }

    private int GetValidIntegerValue(string prompt)
    {
        int option;
        bool result;
        do
        {
            Console.Write(prompt);
            string input = Console.ReadLine();
            result = int.TryParse(input, out option);
            if (!result || option <= 0)
            {
                Console.WriteLine("Ошибка! Пожалуйста, введите целое положительное число.");
            }
        }
        while (!result || option <= 0);
        return option;
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.Title = "Распределение работ по работникам";
        AssignmentProblem manager = new AssignmentProblem();
        manager.Dialogue();
    }
}

