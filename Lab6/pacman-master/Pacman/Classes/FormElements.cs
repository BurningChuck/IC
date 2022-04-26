using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Drawing;

namespace Pacman
{
    class FormElements
    {
        public Label PlayerOneScoreText = new Label();
        public Label HighScoreText = new Label();

        public void CreateFormElements(Form formInstance)
        {
            PlayerOneScoreText.ForeColor = System.Drawing.Color.White;
            PlayerOneScoreText.Font = new System.Drawing.Font("Folio XBd BT", 14);
            PlayerOneScoreText.Top = 0;
            PlayerOneScoreText.Left = 0;
            PlayerOneScoreText.Height = 0;
            PlayerOneScoreText.Width = 0;
            PlayerOneScoreText.Text = "1UP";
            //formInstance.Controls.Add(PlayerOneScoreText);

            HighScoreText.ForeColor = System.Drawing.Color.White;
            HighScoreText.Font = new System.Drawing.Font("Folio XBd BT", 14);
            HighScoreText.Top = 5;
            HighScoreText.Left = 155;
            HighScoreText.Height = 20;
            HighScoreText.Width = 200;
            HighScoreText.Text = "HIGH SCORE";
            //formInstance.Controls.Add(HighScoreText);
        }
    }
}
