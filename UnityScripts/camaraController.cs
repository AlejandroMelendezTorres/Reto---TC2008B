using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class camaraController : MonoBehaviour
{
    public Camera[] lista;
    int index = 0;
    // Start is called before the first frame update
    void Start()
    {
        lista[0].enabled = true;
        lista[0].GetComponent<AudioListener>().enabled = true;
        lista[1].enabled = false;
        lista[1].GetComponent<AudioListener>().enabled = false;
        lista[2].enabled = false;
        lista[2].GetComponent<AudioListener>().enabled = false;
        lista[3].enabled = false;
        lista[3].GetComponent<AudioListener>().enabled = false;
        lista[4].enabled = false;
        lista[4].GetComponent<AudioListener>().enabled = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            lista[index].enabled = false;
            lista[index].GetComponent<AudioListener>().enabled = false;
            if (index == lista.Length-1)
            {
                index = 0;
            }
            else
            {
                index++;
            }
            lista[index].enabled = true;
            lista[index].GetComponent<AudioListener>().enabled = true;
        }

       if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            lista[index].enabled = false;
            lista[index].GetComponent<AudioListener>().enabled = false;
            if (index == 0)
            {
                index = lista.Length-1;
            } else
            {
                index--;
            }
            lista[index].enabled = true;
            lista[index].GetComponent<AudioListener>().enabled = true;
        }
    }
}
