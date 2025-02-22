using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AT_Proj1
{
    public partial class EnterTImes : Form
    {
        public EnterTImes()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                int t1 = int.Parse(textBox1.Text);
                int t2 = int.Parse(textBox2.Text);
                int t3 = int.Parse(textBox3.Text);

                Form1 form = new Form1(t1, t2, t3);
                form.Show();
            }
            catch { }

        }
    }
}
