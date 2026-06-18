import numpy as np
import nidaqmx
import nidaqmx.constants as const
# import matplotlib.pyplot as plt

amplitude = 1   # V peak
points = 30     # samples per cycle
cycles = 10
dev = "Dev1"
output = "ao0"
input1 = "ai4"
input2 = "ai2"
freq_start = 1
freq_end = 5000
num_data_points = 20

total_points = points*cycles
ratio_list = []
U_input_list = []
U_output_list = []
frequency_list = np.logspace(
    np.log10(freq_start),
    np.log10(freq_end),
    num=num_data_points
)
for frequency in frequency_list:
    fs = frequency * points
    
    waveform = amplitude * np.sin(
        np.linspace(0, 2*np.pi, points, endpoint=False)
    )
    
    with nidaqmx.Task() as ao, nidaqmx.Task() as ai:
        ao.ao_channels.add_ao_voltage_chan(f"{dev}/{output}")
        ao.timing.cfg_samp_clk_timing(
            rate=fs,
            sample_mode=const.AcquisitionType.CONTINUOUS,
            samps_per_chan=points
        )
        ai.ai_channels.add_ai_voltage_chan(
            f"{dev}/{input1}",
            terminal_config=const.TerminalConfiguration.DIFF
        )
        ai.ai_channels.add_ai_voltage_chan(
            f"{dev}/{input2}",
            terminal_config=const.TerminalConfiguration.DIFF
        )
        ai.timing.cfg_samp_clk_timing(
            rate=fs,
            source=f"/{dev}/ao/SampleClock",
            sample_mode=const.AcquisitionType.CONTINUOUS,
            samps_per_chan=points
        )      
        ao.write(waveform, auto_start=False)
        ai.start()
        ao.start()        
        print("Generating sine wave..., Hz=", frequency)
        
        try:
            data = ai.read(number_of_samples_per_channel=total_points)
            ai_ch0 = data[0]
            ai_ch1 = data[1]
            
            U_input = np.sqrt(np.mean(np.square(ai_ch1)))
            U_output = np.sqrt(np.mean(np.square(ai_ch0)))
            print(f"U_input RMS: {U_input:.3f} V, U_output RPM: {U_output:.3f} V")
            U_input_list.append(U_input)
            U_output_list.append(U_output)
        except KeyboardInterrupt:
            pass
        
with open("output.csv", "w") as f:
    f.write("Frequency\tU_input\tU_output\n")
    for frequency, U_input, U_output in zip(frequency_list, U_input_list, U_output_list):
        f.write(f"{frequency}\t{U_input}\t{U_output}\n")
        
# ratio_list = [U_output_list[i]/U_input_list[i] for i in range(0, len(U_output_list))]
# plt.scatter(frequency_list, ratio_list)
# plt.plot(frequency_list, ratio_list)
# plt.xscale("log")
# plt.grid(True, which="both")
# plt.title("Gain vs frequency")
# plt.xlabel("Frequency, Hz")
# plt.ylabel("Gain, U_output (RMS) / U_input (RMS)")
