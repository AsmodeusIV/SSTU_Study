namespace AT_Proj1
{
    public partial class Form1 : Form
    {
        //FSM fsm;
        FSM_Table fsm;
        DateTime start;
        public Form1(int t1, int t2, int t3)
        {
            InitializeComponent();

            //fsm = new FSM(t1,t2,t3);
            fsm = new FSM_Table(t1, t2, t3);

            timer1.Interval = 1001;
            //Task.Run(() => fsm.Work()); 
            //timer1.Tick += Process;
            timer1.Tick += Process1;
            timer1.Start();
            start = DateTime.Now;
        }
        /*
        private void Process(object sender, EventArgs e)
        {

            string state = fsm.GetCurrentState();
            label1.Text = (DateTime.Now - start).ToString(@"hh\:mm\:ss");
            if (state == "1010")
            {
                pictureBox1.Image = Properties.Resources.red_dop_1;
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
        */
        private void Process1(object sender, EventArgs e)
        {

            string state = fsm.ManualEntry();
            label1.Text = "Время: " + (DateTime.Now - start).ToString(@"hh\:mm\:ss");
            if (state == "1010")
            {
                pictureBox1.Image = Properties.Resources.red_dop_1;
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

        private void pictureBox3_Click(object sender, EventArgs e)
        {

        }
    }
}
