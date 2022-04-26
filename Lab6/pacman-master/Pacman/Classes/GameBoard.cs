using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Pacman
{
    public class GameBoard
    {
        public PictureBox BoardImage = new PictureBox();
        public int[,] Matrix = new int[12,12];

        public void CreateBoardImage(Form formInstance, int Level)
        {
            InitialiseBoardMatrix(2);
            // Create Board Image
             int m_iSize = 20;
            BoardImage.Name = "BoardImage";
            BoardImage.SizeMode = PictureBoxSizeMode.AutoSize;
            BoardImage.Location = new Point(0, 0);
           
            Bitmap bm = new Bitmap(500,500);
            using (Graphics myGraphics = Graphics.FromImage(bm))
            {
                myGraphics.SmoothingMode = SmoothingMode.AntiAlias;

                for (int i = 0; i < 12; i++)
                    for (int j = 0; j < 12; j++)
                    {
                        // print grids
                        // myGraphics.DrawRectangle(new Pen(Color.Black) , j*m_iSize, i*m_iSize, m_iSize, m_iSize);
                        // print walls
                        if (Matrix[i, j] == 10)
                            myGraphics.FillEllipse(new SolidBrush(Color.Blue), j * m_iSize + 1,i * m_iSize + 1, m_iSize - 1, m_iSize - 1);
                            //myGraphics.FillRectangle(new SolidBrush(Color.Blue), j * m_iSize + 1, i * m_iSize + 1, m_iSize - 1, m_iSize - 1);
                        //print path
                        
                    }
                BoardImage.Image = bm;
            }

            formInstance.Controls.Add(BoardImage);
        }

        public Tuple<int,int> InitialiseBoardMatrix(int Level)
        {
            // Initialise Game Board Matrix
            switch (Level)
            {
                
                case 2:
                    {
                        Matrix = new int[,] {
                        { 10,10,10,10,10,10,10,10,10,10,10,10},
                        { 10,01,01,01,01,01,01,01,01,01,01,10},
                        { 10,10,10,01,10,01,01,01,10,10,01,10},
                        { 10,01,01,01,10,01,10,01,01,10,01,10},
                        { 10,01,10,10,10,01,10,01,10,10,01,10},
                        { 10,01,10,10,10,01,10,01,01,01,01,10},
                        { 10,01,01,01,01,01,10,01,10,10,10,10},
                        { 10,10,10,10,10,10,10,01,01,01,01,10},
                        { 10,01,01,01,01,01,01,01,01,10,01,10},
                        { 10,01,01,01,01,01,01,10,01,01,01,10},
                        { 10,03,01,10,10,01,01,01,10,01,01,10},
                        { 10,10,10,10,10,10,10,10,10,10,10,10}};
                    break;
                    }
            }
            int StartX = 0;
            int StartY = 0;
            for (int y=0; y<12; y++)
            {
                for (int x=0; x<12; x++)
                {
                    if (Matrix[y, x] == 3) { StartX = x; StartY = y;}
                }
            }
            Tuple<int,int> StartLocation = new Tuple<int,int> (StartX, StartY);
            return StartLocation;
        }
    }
}
