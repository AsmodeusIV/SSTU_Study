using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AT_Proj1
{
    internal class FSM_Table
    {
        private int curState = 0;
        private readonly int t1, t2, t3;
        private bool work = true;
        private State[] states;
        public FSM_Table(int t1, int t2, int t3)
        {
            this.t1 = t1;
            this.t2 = t2;
            this.t3 = t3;

            states = new State[t1 + t2 + t3];
            for(int i = 0; i < states.Length; i++)
            {
                states[i] = new State();
                states[i].NextState = (i + 1)%(t1+t2+t3);
                if (i >= 0 && i < t1)
                {
                    states[i].Output = "1010";
                }
                else if (i >= t1 && i < t1 + t2)
                {
                    states[i].Output = "0011";
                }
                else if (i >= t1 + t2 && i < t1 + t2 + t3)
                {
                    states[i].Output = "0100";
                }
            }
        }
        public string ManualEntry()
        {
            string Result = states[curState].Output;
            curState = states[curState].NextState;
            return Result;
        }
    }
}
