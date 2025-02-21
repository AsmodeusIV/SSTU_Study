namespace AT_Proj1
{
    public partial class Form1 : Form
    {
        FSM fsm;
        DateTime start;
        public Form1()
        {
            InitializeComponent();
            
            fsm = new FSM(10, 10, 10);

            Task.Run(() => fsm.Work()); 
            
            timer1.Interval = 1000;
            timer1.Tick += Process;
            timer1.Start();
            start = DateTime.Now;
        }

        private void Process(object sender, EventArgs e)
        {
            
            string state = fsm.GetCurrentState();
            label1.Text = (DateTime.Now - start).ToString(@"hh\:mm\:ss");
            if (state == "1010") {
                pictureBox1.Image = Properties.Resources.red_dop;
                pictureBox2.Image = Properties.Resources.green;
                pictureBox3.Image = Properties.Resources.red;
            }
            else if (state == "0011")
            {
                pictureBox1.Image = Properties.Resources.green_dop;
                pictureBox2.Image = Properties.Resources.red;
                pictureBox3.Image = Properties.Resources.red;
            }
            else if (state == "0100")
            {
                pictureBox1.Image = Properties.Resources.red_dop;
                pictureBox2.Image = Properties.Resources.red;
                pictureBox3.Image = Properties.Resources.green;
            }
        }

    }
}
