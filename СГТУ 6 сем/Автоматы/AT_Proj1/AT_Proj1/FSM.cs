using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AT_Proj1
{
    internal class FSM
    {
        private int state = 0;
        private readonly int t1, t2, t3;
        public FSM(int t1, int t2, int t3)
        {
            this.t1 = t1;
            this.t2 = t2;
            this.t3 = t3;
        }

        private void ChangeState()
        {
            state++;
            state %= (t1 + t2 + t3);
        }

        public string GetCurrentState()
        {
            if (state >= 0 && state < t1)
            {
                return "1010";
            }
            else if (state >= t1 && state < t1 + t2)
            {
                return "0011";
            }
            else if (state >= t1 + t2 && state < t1 + t2 + t3)
            {
                return "0100";
            }
            return "-1";
        }

        public async void Work()
        {
            while (true) {
                ChangeState();
                Thread.Sleep(1000);
            }
        }
    }
}
