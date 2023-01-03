
myString = 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm'
max_length = 30
for (int i = 0; i < myString.Length; i += max_length )
            {
                if (myString[i] != ' ' || myString[i] != ',')
                {
                    while( i > 1)
                    {
                        i--;
                        if (myString[i] == ' ' || myString[i] == ',')
                        {
                            break;
                        }
                    }
                }
                myString.Insert(i + 1, Environment.NewLine);
            }
            label1.Text = myString;
            
            
print (myString)   