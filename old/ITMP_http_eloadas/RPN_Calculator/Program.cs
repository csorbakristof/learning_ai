using System;
using System.Collections.Generic;

namespace RPNCalculator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== RPN (Reverse Polish Notation) Számológép ===");
            Console.WriteLine("Példa használat: 3 4 + 2 *");
            Console.WriteLine("Operátorok: +, -, *, /");
            Console.WriteLine("Kilépés: 'exit' parancs\n");

            // Fő program ciklus - fut amíg a felhasználó ki nem lép
            while (true)
            {
                Console.Write("RPN kifejezés: ");
                string input = Console.ReadLine();

                // Kilépés kezelése
                if (input?.ToLower() == "exit")
                {
                    Console.WriteLine("Viszlát!");
                    break;
                }

                // Üres bemenet ellenőrzése
                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine("Hiba: Üres bemenet!\n");
                    continue;
                }

                try
                {
                    // RPN kifejezés kiértékelése
                    double result = EvaluateRPN(input);
                    Console.WriteLine($"Eredmény: {result}\n");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Hiba: {ex.Message}\n");
                }
            }
        }

        /// <summary>
        /// RPN kifejezés kiértékelése stack segítségével
        /// </summary>
        /// <param name="expression">Az RPN kifejezés szöveges formában</param>
        /// <returns>A kifejezés eredménye</returns>
        static double EvaluateRPN(string expression)
        {
            // Stack létrehozása a számok tárolására
            Stack<double> stack = new Stack<double>();

            // Kifejezés felbontása szóközök mentén
            string[] tokens = expression.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);

            // Minden token feldolgozása
            foreach (string token in tokens)
            {
                // Ellenőrizzük, hogy a token szám-e
                if (double.TryParse(token, out double number))
                {
                    // Ha szám, tegyük a verembe
                    stack.Push(number);
                }
                // Ha nem szám, akkor operátornak kell lennie
                else if (IsOperator(token))
                {
                    // Ellenőrizzük, hogy van-e legalább 2 operandus a veremben
                    if (stack.Count < 2)
                    {
                        throw new InvalidOperationException(
                            $"Nincs elég operandus a(z) '{token}' operátorhoz. Legalább 2 szükséges.");
                    }

                    // Kivesszük a két felső elemet (fordított sorrendben!)
                    // Az utoljára betett elem lesz a második operandus
                    double operand2 = stack.Pop();
                    double operand1 = stack.Pop();

                    // Művelet végrehajtása az operátor alapján
                    double result = PerformOperation(operand1, operand2, token);

                    // Eredmény visszatétele a verembe
                    stack.Push(result);
                }
                else
                {
                    // Ha nem szám és nem operátor, akkor érvénytelen bemenet
                    throw new ArgumentException($"Érvénytelen token: '{token}'");
                }
            }

            // A végén pontosan 1 elemnek kell maradnia a veremben
            if (stack.Count != 1)
            {
                throw new InvalidOperationException(
                    $"Hibás kifejezés! A veremben {stack.Count} elem maradt 1 helyett.");
            }

            // Az egyetlen megmaradt elem az eredmény
            return stack.Pop();
        }

        /// <summary>
        /// Ellenőrzi, hogy a token operátor-e
        /// </summary>
        static bool IsOperator(string token)
        {
            return token == "+" || token == "-" || token == "*" || token == "/";
        }

        /// <summary>
        /// Művelet végrehajtása két operanduson
        /// </summary>
        /// <param name="operand1">Első operandus</param>
        /// <param name="operand2">Második operandus</param>
        /// <param name="operatorSymbol">Operátor (+, -, *, /)</param>
        /// <returns>A művelet eredménye</returns>
        static double PerformOperation(double operand1, double operand2, string operatorSymbol)
        {
            switch (operatorSymbol)
            {
                case "+":
                    return operand1 + operand2;

                case "-":
                    return operand1 - operand2;

                case "*":
                    return operand1 * operand2;

                case "/":
                    // Nullával való osztás ellenőrzése
                    if (operand2 == 0)
                    {
                        throw new DivideByZeroException("Nullával való osztás!");
                    }
                    return operand1 / operand2;

                default:
                    throw new ArgumentException($"Ismeretlen operátor: '{operatorSymbol}'");
            }
        }
    }
}
